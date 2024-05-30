import atexit
import signal
from pathlib import Path

import toml
from rich.console import Console

from .__about__ import __name__

console: Console = Console()

CONFIG_PATH = Path.home() / ".config" / __name__ / "config.toml"
SETTINGS = {
    "git_directories": [],
    "git_author": None,
    "censor_author": False,
    "date_format": r"%Y-%m-%d",
}

def load_config():
    if CONFIG_PATH.exists():
        with CONFIG_PATH.open("r", encoding="utf-8") as f:
            config = toml.load(f)
            SETTINGS.update(config)

load_config()

def save_config():
    CONFIG_PATH.parent.mkdir(exist_ok=True, parents=True)

    with CONFIG_PATH.open("w", encoding="utf-8") as f:
        toml.dump(SETTINGS, f)


atexit.register(save_config)
signal.signal(signal.SIGTERM, save_config)
signal.signal(signal.SIGINT, save_config)
