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
CLONE_OWNERS = {}

mongo_async_cli = _mongo_async_(MONGO_DB_URL)
mongodb = mongo_async_cli.badmundaxdb
db = mongodb.Anonymous
mongodb = mongodb.program

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
from BADUC.core.logger import LOGGER
logs = LOGGER


# Plugins
from BADUC.core.config import PLUGINS
plugs = PLUGINS


# Variables
from BADUC.core import config
vars = config


#clone

cloneownerdb = db.clone_owners

CLONE_OWNERS = {}

async def load_clone_owners():
    async for entry in cloneownerdb.find():
        bot_id = entry.get("bot_id")
        user_id = entry.get("user_id")
        if bot_id and user_id:
            CLONE_OWNERS[bot_id] = user_id

async def save_clonebot_owner(bot_id, user_id):
    await cloneownerdb.update_one(
        {"bot_id": bot_id},
        {"$set": {"user_id": user_id}},
        upsert=True
    )
async def get_clone_owner(bot_id):
    data = await cloneownerdb.find_one({"bot_id": bot_id})
    if data:
        return data["user_id"]
    return None

async def delete_clone_owner(bot_id):
    await cloneownerdb.delete_one({"bot_id": bot_id})
    CLONE_OWNERS.pop(bot_id, None)

async def save_idclonebot_owner(clone_id, user_id):
    await cloneownerdb.update_one(
        {"clone_id": clone_id},
        {"$set": {"user_id": user_id}},
        upsert=True
    )

async def get_idclone_owner(clone_id):
    data = await cloneownerdb.find_one({"clone_id": clone_id})
    if data:
        return data["user_id"]
    return None
