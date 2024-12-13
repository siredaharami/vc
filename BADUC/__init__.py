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
__version__ = "v3.0.0"

spam_chats = []
SUDOERS = SUDOERS
SUDOERS.append(OWNER_ID)



mongo_async_cli = _mongo_async_(MONGO_DB_URL)
mongodb = mongo_async_cli.badmundaxdb


# import 

# All Clients
from BADUC.core.clients import (
    app, bot, call
)
app = app
bot = bot
call = call





# Edit Or Reply
from BADUC.functions.events import (
    edit_or_reply
)
eor = edit_or_reply


# Logger
from BADUC.logger import LOGGER
logs = LOGGER


# Plugins
from BADUC.core.config import PLUGINS
plugs = PLUGINS


# Variables
from BADUC.core import config
vars = config
