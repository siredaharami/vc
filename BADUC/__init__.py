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
__version__ = {
    "Pbxbot": "3.0",
    "pyrogram": pyrogram_version,
    "python": python_version(),
}

spam_chats = []
SUDO_USER = SUDO_USERS
SUDO_USERS.append(OWNER_ID)



mongo_async_cli = _mongo_async_(MONGO_DB_URL)
mongodb = mongo_async_cli.badmundaxdb


from BADUC.functions.text import (
    super_user_only, sudo_user
)
super_user_only = super_user_only
sudo_user = sudo_user
