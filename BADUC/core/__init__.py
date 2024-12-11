from .clients import app, bot, call
from .config import *
from .logger import LOGGER
logs = LOGGER

from BADUC.core.config import PLUGINS
plugs = PLUGINS

from .core import config
vars = config

from .command import cdx, rgx, cdz

__all__ = [
    "app",
    "bot",
    "call",
    "Config",
    "LOGGER",
    "rgx",
    "cdz",
    "cdx",
]
