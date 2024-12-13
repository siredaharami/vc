import os
import time
from .core.config import *
from .core.config import MONGO_DB_URL
from platform import python_version
from typing import Union, List, Pattern
from pyrogram import __version__ as pyrogram_version
from motor.motor_asyncio import AsyncIOMotorClient as _mongo_async_
from pytgcalls import PyTgCalls, filters as pytgfl
from pytgcalls.types import ChatUpdate, Update, GroupCallConfig
from pytgcalls.types import Call, MediaStream, AudioQuality, VideoQuality

# Ai-Userbot Version
__version__ = "v2.1.0"

spam_chats = []
SUDO_USER = SUDO_USERS
SUDO_USERS.append(OWNER_ID)



from BADUC.core.clients import (
    app, bot, call
)
app = app
bot = bot
call = call


from BADUC.functions.events import (
    edit_or_reply
)
eor = edit_or_reply


from BADUC.core.logger import LOGGER
logs = LOGGER

from BADUC.core.config import PLUGINS
plugs = PLUGINS

from BADUC.core import config
vars = config

