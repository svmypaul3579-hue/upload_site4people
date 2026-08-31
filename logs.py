import os
import inspect
from datetime import datetime
# pyrefly: ignore [missing-import]
from rich.console import Console
from rich.panel import Panel
from rich.theme import Theme


LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, "log_{}.log".format(datetime.now().strftime("%Y-%m-%d_%H-%M-%S")))

os.makedirs(LOG_DIR, exist_ok=True)


def _get_caller_info():
    frame = inspect.stack()[2]
    filename = os.path.basename(frame.filename)
    lineno = frame.lineno
    return filename, lineno


def _format_message(message, *args):
    if args:
        try:
            return message % args
        except (TypeError, ValueError):
            return str(message) + " " + " ".join(str(arg) for arg in args)
    return str(message)


def _log_to_file(level, message, filename, lineno):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write("[" + ts + "] [" + level.upper() + "] [" + filename + ":" + str(lineno) + "] " + message + chr(10))


custom_theme = Theme({
    "info": "bold blue",
    "success": "bold green",
    "warning": "bold yellow",
    "error": "bold red",
    "debug": "dim cyan",
    "highlight": "bold magenta",
})

console = Console(theme=custom_theme)


def info(message, *args):
    message = _format_message(message, *args)
    filename, lineno = _get_caller_info()
    console.print("[info]>> INFO:[/info] [" + filename + ":" + str(lineno) + "] " + message)
    _log_to_file("info", message, filename, lineno)


def success(message, *args):
    message = _format_message(message, *args)
    filename, lineno = _get_caller_info()
    console.print("[success]>> SUCCESS:[/success] [" + filename + ":" + str(lineno) + "] " + message)
    _log_to_file("success", message, filename, lineno)


def warning(message, *args):
    message = _format_message(message, *args)
    filename, lineno = _get_caller_info()
    console.print("[warning]>> WARNING:[/warning] [" + filename + ":" + str(lineno) + "] " + message)
    _log_to_file("warning", message, filename, lineno)


def error(message, *args):
    message = _format_message(message, *args)
    filename, lineno = _get_caller_info()
    console.print("[error]>> ERROR:[/error] [" + filename + ":" + str(lineno) + "] " + message)
    _log_to_file("error", message, filename, lineno)


def debug(message, *args):
    message = _format_message(message, *args)
    filename, lineno = _get_caller_info()
    console.print("[debug]>> DEBUG:[/debug] [" + filename + ":" + str(lineno) + "] " + message)
    _log_to_file("debug", message, filename, lineno)


def exception(message, *args):
    message = _format_message(message, *args)
    filename, lineno = _get_caller_info()
    console.print("[error]>> ERROR:[/error] [" + filename + ":" + str(lineno) + "] " + message)
    _log_to_file("error", message, filename, lineno)


def highlight(message, *args):
    message = _format_message(message, *args)
    filename, lineno = _get_caller_info()
    console.print(Panel("[blue]" + message + "[/blue] [" + filename + ":" + str(lineno) + "]", expand=False, border_style="light_green"))
    _log_to_file("highlight", message, filename, lineno)


def print_traceback():
    console.print_exception()


