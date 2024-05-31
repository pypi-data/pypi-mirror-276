import inspect
import logging
import sys
from pathlib import Path
from typing import Optional

import structlog
from rich.console import Console, ConsoleRenderable, Group, RenderableType
from rich.highlighter import ReprHighlighter
from rich.pretty import Pretty
from rich.styled import Styled
from rich.table import Table
from rich.text import Text
from rich.theme import Theme
from rich.traceback import Traceback
from structlog.processors import _figure_out_exc_info
from structlog.typing import EventDict, WrappedLogger


def setup_logging(
    log_level: str = "INFO",
    pkg2loglevel: dict[str, str] | None = None,
):
    # intercept everything at the root logger
    logging.root.handlers = [InterceptHandler(log_level, pkg2loglevel)]
    logging.root.setLevel(0)

    # remove every other logger's handlers
    # and propagate to root logger
    for name in logging.root.manager.loggerDict.keys():
        logging.getLogger(name).handlers = []
        logging.getLogger(name).propagate = True

    # get the global log level and convert it to a number
    level = logging._nameToLevel.get(log_level)
    assert level, f"Invalid log level: {log_level}"
    # configure structlog
    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.processors.add_log_level,
            structlog.processors.StackInfoRenderer(),
            structlog.processors.CallsiteParameterAdder(),
            structlog.dev.set_exc_info,
            structlog.processors.TimeStamper(fmt="%Y-%m-%d %H:%M:%S", utc=False),
            # structlog.dev.ConsoleRenderer(),
            RichConsoleRenderer(),
        ],
        wrapper_class=structlog.make_filtering_bound_logger(level),
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(),
        cache_logger_on_first_use=False,
    )


def get_log_level_number(log_level_str: str):
    # Normalize the input to ensure compatibility
    normalized_log_level = log_level_str.upper()

    # Get the numeric value of the log level
    level_number = logging.getLevelName(normalized_log_level)
    if isinstance(level_number, int):
        return level_number
    else:
        raise ValueError(f"Invalid log level: {log_level_str}")


class RichConsoleRenderer:
    """
    adapted from https://github.com/Textualize/rich/blob/master/rich/_log_render.py#L14
    """

    def __init__(self) -> None:
        self.max_path_segments = 1
        self.show_time = True
        self.show_level = True
        self.show_path = True
        self.time_format = "%H:%M:%S"
        self.omit_repeated_times = True
        self.level_width = 2
        self._last_time: Optional[Text] = None
        self.repr_highlighter = ReprHighlighter()
        self.console = Console()

    def level2color(self, level: str) -> str:
        match level:
            case "DEBUG":
                color = "blue"
            case "INFO":
                color = "green"
            case "WARNING":
                color = "yellow"
            case "ERROR":
                color = "red"
            case "CRITICAL":
                color = "red"
            case _:
                color = "white"

        return color

    def print_log_error(self, msg: str):
        self.console.print(f"Logging error: {msg}", style="red bold")

    def get_caller(self, package_name: str | None) -> tuple[str, str, int] | None:
        # Fix frame
        frame, depth = inspect.currentframe(), 0
        while frame and (
            depth == 0
            or frame.f_code.co_filename == logging.__file__
            or frame.f_code.co_filename == __file__
            or "structlog" in frame.f_code.co_filename
        ):
            frame = frame.f_back
            depth += 1

        if not frame:
            self.print_log_error("Frame is None")
            return None

        lineno = int(frame.f_lineno)
        path = frame.f_code.co_filename

        # Get the package name
        if not package_name:
            module = sys.modules[frame.f_globals["__name__"]]
            if module:
                package_name = module.__package__ or module.__name__

        if not package_name:
            self.print_log_error("Could not determine package name")
            return None

        return package_name, path, lineno

    def run(self, event_dict: EventDict):
        pkgname = event_dict.pop("pkgname", None)

        exclude = [
            "pathname",
            "level",
            "event",
            "timestamp",
            "lineno",
            "module",
            "func_name",
            "process",
            "thread",
            "thread_name",
            "process_name",
            "filename",
            "exc_info",
        ]
        ctx = {k: v for k, v in event_dict.items() if k not in exclude}
        level: str = event_dict["level"].upper()
        color = self.level2color(level)

        caller = self.get_caller(pkgname)
        if not caller:
            self.print_log_error("Could not determine caller")
            return

        pkgname, path, lineno = caller

        ts: str = event_dict["timestamp"]
        event: str = event_dict["event"]

        header = self.create_header(ts, level, pkgname, path, lineno, event)

        # handle exceptions
        tb = None
        exc_info = event_dict.get("exc_info", None)
        if exc_info:
            exc_type, exc_value, traceback = _figure_out_exc_info(exc_info)
            if exc_type and exc_value and traceback:
                tb = Traceback()
            else:
                raise NotImplementedError("exc_info tuple is incomplete.")

        renderables: list[ConsoleRenderable] = [header]

        if ctx:
            renderables.append(self.create_ctx(**ctx))
        if tb:
            renderables.append(tb)

        group = Group(*renderables)

        with self.console.use_theme(
            theme=Theme(
                {
                    "repr.str": "grey58",
                    # "repr.str": f"dim {color}",
                    # "repr.indent": f"dim {color}",
                    "repr.indent": "dim grey58",
                    # "repr.brace": f"{color}",
                    # "repr.comma": f"dim {color}",
                    # "repr.brace": "dim white",
                    "log.level": f"bold {color}",
                    # "rule.line": f"{color}",
                    # "rule.text": f"bold {color}",
                    "ctx.keys": "dim wheat1",
                    # "ctx.vals": "dim red",
                    # "log.pkgname": "light_goldenrod2",
                }
            )
        ):
            self.console.print(group)

    def __call__(self, logger: WrappedLogger, name: str, event_dict: EventDict) -> str:
        with self.console.capture() as capture:
            self.run(event_dict)
        return capture.get().strip()

    def create_header(
        self, ts: str, level: str, pkgname: str, path: str, lineno: int, event: str
    ) -> "Table":
        table = Table.grid(padding=(0, 1))
        table.expand = True

        # ts
        table.add_column(style="log.time")
        # level
        table.add_column(style="log.level", width=5)
        table.add_column(ratio=1, overflow="fold")
        table.add_column(style="")

        row: list["RenderableType"] = []

        # ts
        row.append(ts)
        # level
        row.append(level)

        # pkgname+path+lineno
        abs_path = Path(path).absolute()
        path = str(abs_path)
        # shorten path
        if self.max_path_segments:
            path_segments = path.split("/")
            if len(path_segments) > self.max_path_segments:
                path = "/".join(path_segments[-self.max_path_segments :])

        # event
        row.append(self.repr_highlighter(event))
        row.append(
            f"[light_goldenrod2]{pkgname}[/light_goldenrod2] [link=file://{abs_path}:{lineno}]{path}:{lineno}[/link]"
        )

        table.add_row(*row)
        return table

    def create_ctx(self, **kwargs) -> "Table":
        table = Table.grid(padding=(0, 2))
        table.expand = True

        table.add_column(justify="right", width=8, style="ctx.keys")
        table.add_column(ratio=1)

        for k, v in kwargs.items():
            v = (
                Styled(
                    Pretty(
                        v,
                        expand_all=True,
                        indent_guides=True,
                    ),
                    style="repr.comma",
                )
                if not isinstance(v, str)
                else Text(v, style="repr.str")
            )
            table.add_row(k, v)

        return table


class InterceptHandler(logging.Handler):
    def __init__(
        self, log_level: str = "INFO", pkg2loglevel: dict[str, str] | None = None
    ):
        super().__init__()

        self.pkgname2levelno = (
            {pkg: get_log_level_number(level) for pkg, level in pkg2loglevel.items()}
            if pkg2loglevel
            else None
        )
        self.log_level_no = get_log_level_number(log_level)
        self.log: structlog.stdlib.BoundLogger = structlog.get_logger()

    def emit(self, record: logging.LogRecord) -> None:
        levelno = record.levelno
        pkgname = record.name.split(".")[0]

        if self.pkgname2levelno and pkgname in self.pkgname2levelno:
            if self.pkgname2levelno[pkgname] > levelno:
                return
        elif self.log_level_no > levelno:
            return

        self.log.log(levelno, record.getMessage(), pkgname=pkgname)
