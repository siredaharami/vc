from pymongo import MongoClient
from pyrogram import Client, filters
from pyrogram.types import Message

from BADUC import SUDOERS
from BADUC.core.clients import app
from BADUC.core.config import LOG_GROUP_ID as LOGGER_ID, MONGO_DB_URL  # Importing MONGO_DB_URL from config
from BADUC.core.command import *

# MongoDB setup using MONGO_DB_URL from config
client = MongoClient(MONGO_DB_URL)
db = client["bot_database"]
welcome_col = db["welcome_messages"]
goodbye_col = db["goodbye_messages"]

# Utility functions
def get_welcome(chat_id):
    return welcome_col.find_one({"chat_id": chat_id})

def set_welcome(chat_id, message_id):
    welcome_col.update_one({"chat_id": chat_id}, {"$set": {"message_id": message_id}}, upsert=True)

def delete_welcome(chat_id):
    welcome_col.delete_one({"chat_id": chat_id})

def get_goodbye(chat_id):
    return goodbye_col.find_one({"chat_id": chat_id})

def set_goodbye(chat_id, message_id):
    goodbye_col.update_one({"chat_id": chat_id}, {"$set": {"message_id": message_id}}, upsert=True)

def delete_goodbye(chat_id):
    goodbye_col.delete_one({"chat_id": chat_id})

GREETINGS_FORMATTINGS = """
`{first}` - __First name of the user who joined/left.__
`{last}` - __Last name of the user who joined/left.__
`{fullname}` - __Full name of the user who joined/left.__
`{mention}` - __Mentions the user who joined/left.__
`{username}` - __Username of the user who joined/left.__
`{userid}` - __ID of the user who joined/left.__
`{chatname}` - __Name of the chat.__
`{chatid}` - __ID of the chat.__
"""

@app.on_message(bad(["greetings"]) & (filters.me | filters.user(SUDOERS)))
async def greetings_format(_, message: Message):
    await message.edit(GREETINGS_FORMATTINGS)


# Welcome Commands
@app.on_message(bad(["setwelcome"]) & (filters.me | filters.user(SUDOERS)))
async def setwelcome(client: Client, message: Message):
    if not message.reply_to_message:
        return await message.edit("Reply to a message to set it as the welcome message.")

    forwarded_message = await message.reply_to_message.forward(LOGGER_ID)
    set_welcome(message.chat.id, forwarded_message.id)
    await message.edit(f"Welcome message set for {message.chat.title}.")

@app.on_message(bad(["delwelcome"]) & (filters.me | filters.user(SUDOERS)))
async def delwelcome(client: Client, message: Message):
    if get_welcome(message.chat.id):
        delete_welcome(message.chat.id)
        await message.edit("Welcome message deleted.")
    else:
        await message.edit("No welcome message set for this chat.")

@app.on_message(bad(["welcome"]) & (filters.me | filters.user(SUDOERS)))
async def showwelcome(client: Client, message: Message):
    welcome = get_welcome(message.chat.id)
    if not welcome:
        return await message.edit("No welcome message set for this chat.")
    msg = await client.get_messages(LOGGER_ID, welcome["message_id"])
    await msg.copy(message.chat.id)
    await message.edit("Welcome message sent.")

# Goodbye Commands
@app.on_message(bad(["setgoodbye"]) & (filters.me | filters.user(SUDOERS)))
async def setgoodbye(client: Client, message: Message):
    if not message.reply_to_message:
        return await message.edit("Reply to a message to set it as the goodbye message.")

    forwarded_message = await message.reply_to_message.forward(LOGGER_ID)
    set_goodbye(message.chat.id, forwarded_message.id)
    await message.edit(f"Goodbye message set for {message.chat.title}.")

@app.on_message(bad(["delgoodbye"]) & (filters.me | filters.user(SUDOERS)))
async def delgoodbye(client: Client, message: Message):
    if get_goodbye(message.chat.id):
        delete_goodbye(message.chat.id)
        await message.edit("Goodbye message deleted.")
    else:
        await message.edit("No goodbye message set for this chat.")

@app.on_message(bad(["goodbye"]) & (filters.me | filters.user(SUDOERS)))
async def showgoodbye(client: Client, message: Message):
    goodbye = get_goodbye(message.chat.id)
    if not goodbye:
        return await message.edit("No goodbye message set for this chat.")
    msg = await client.get_messages(LOGGER_ID, goodbye["message_id"])
    await msg.copy(message.chat.id)
    await message.edit("Goodbye message sent.")

# Event Handlers
@app.on_message(filters.new_chat_members & filters.group)
async def welcome_handler(client: Client, message: Message):
    welcome = get_welcome(message.chat.id)
    if not welcome:
        return

    msg = await client.get_messages(LOGGER_ID, welcome["message_id"])
    if not msg:
        return

    # Replace placeholders
    new_member = message.new_chat_members[0]
    text = msg.text or msg.caption
    if text:
        formatted_text = text.format(
            first=new_member.first_name or "User",
            last=new_member.last_name or "",
            fullname=f"{new_member.first_name} {new_member.last_name}".strip(),
            mention=new_member.mention or f"[{new_member.first_name}](tg://user?id={new_member.id})",
            username=f"@{new_member.username}" if new_member.username else "No Username",
            userid=new_member.id,
            chatname=message.chat.title,
            chatid=message.chat.id,
        )
        await message.reply(formatted_text)

@app.on_message(filters.left_chat_member & filters.group)
async def goodbye_handler(client: Client, message: Message):
    goodbye = get_goodbye(message.chat.id)
    if not goodbye:
        return

    msg = await client.get_messages(LOGGER_ID, goodbye["message_id"])
    if not msg:
        return

    # Replace placeholders
    left_member = message.left_chat_member
    text = msg.text or msg.caption
    if text:
        formatted_text = text.format(
            first=left_member.first_name or "User",
            last=left_member.last_name or "",
            fullname=f"{left_member.first_name} {left_member.last_name}".strip(),
            mention=left_member.mention or f"[{left_member.first_name}](tg://user?id={left_member.id})",
            username=f"@{left_member.username}" if left_member.username else "No Username",
            userid=left_member.id,
            chatname=message.chat.title,
            chatid=message.chat.id,
        )
        await message.reply(formatted_text)
