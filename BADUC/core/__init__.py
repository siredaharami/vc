from .clients import app, bot, call
from .config import *
from .logger import LOGGER
logs = LOGGER

from BADUC.core.config import PLUGINS
plugs = PLUGINS

from BADUC.core import config
vars = config

from .command import bad, sukh, abhi

__all__ = [
    "app",
    "bot",
    "call",
    "Config",
    "LOGGER",
    "bad",
    "sukh",
    "abhi",
]
