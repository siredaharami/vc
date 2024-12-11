from typing import Union, List, Pattern
from .core.config import *
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
OWNER_USERNAME = OWNER_USERNAME
SUDO_USERS.append(OWNER_ID)



mongo_async_cli = _mongo_async_(config.MONGO_DB_URL)
mongodb = mongo_async_cli.badmundaxdb


