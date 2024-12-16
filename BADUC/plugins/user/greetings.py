from pymongo import MongoClient
from BADUC import SUDOERS
from BADUC.core.clients import app
from BADUC.core.config import LOG_GROUP_ID as LOGGER_ID, MONGO_DB_URL
from BADUC.core.command import *

from pyrogram import Client, filters
from pyrogram.types import Message

# Default welcome and goodbye messages
WELCOME_MESSAGE = "Welcome {mention} to {chatname}! 🎉"
GOODBYE_MESSAGE = "Goodbye {mention}, we'll miss you in {chatname}. 😢"


# Helper function to format messages
def format_message(template, user, chat):
    return template.format(
        first=user.first_name or "",
        last=user.last_name or "",
        fullname=f"{user.first_name or ''} {user.last_name or ''}".strip(),
        mention=user.mention or user.first_name,
        username=f"@{user.username}" if user.username else "User",
        userid=user.id,
        chatname=chat.title or "this chat",
        chatid=chat.id,
    )

# Welcome new members
@app.on_message(filters.new_chat_members)
async def welcome(client, message: Message):
    print(f"New member(s) joined: {[user.id for user in message.new_chat_members]}")
    for new_member in message.new_chat_members:
        welcome_text = format_message(WELCOME_MESSAGE, new_member, message.chat)
        await message.reply_text(welcome_text)

# Goodbye for leaving members
@app.on_message(filters.left_chat_member)
async def goodbye(client, message: Message):
    user = message.left_chat_member
    print(f"Member left: {user.id}")
    goodbye_text = format_message(GOODBYE_MESSAGE, user, message.chat)
    await message.reply_text(goodbye_text)

