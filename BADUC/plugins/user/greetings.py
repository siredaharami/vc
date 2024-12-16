from pymongo import MongoClient
from pyrogram.types import ChatMemberUpdated, Message
from pyrogram.enums import ChatMemberStatus
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


# Handler for new members joining the group
@app.on_message(filters.new_chat_members)
async def welcome_new_member(client, message: Message):
    new_members = message.new_chat_members
    for member in new_members:
        # Send a welcome message
        await message.reply(f"Hey, {member.first_name}, welcome to this group!")

# Handler for a member leaving the group
@app.on_chat_member_updated
async def farewell_member(client, update: ChatMemberUpdated):
    # Use the ChatMemberStatus enum to check the member's status
    if update.old_chat_member.status == ChatMemberStatus.MEMBER and update.new_chat_member.status == ChatMemberStatus.RESTRICTED:
        user = update.old_chat_member.user
        chat = update.chat
        # Send a farewell message
        await chat.send_message(f"Nice knowing you, {user.first_name}!")
