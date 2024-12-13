from BADUC.core.clients import (
    app, bot, call
)
app = app
bot = bot
call = call

from .logger import LOGGER
logs = LOGGER

from BADUC.core.config import PLUGINS
plugs = PLUGINS

from BADUC.core import config
vars = config

from BADUC.functions.events import (
    edit_or_reply
)
eor = edit_or_reply
