import sqlite3
from pyrogram import Client, filters
from pyrogram.types import Message

from BADUC import SUDOERS
from BADUC.core.clients import app
from BADUC.core.config import LOG_GROUP_ID as LOGGER_ID
from BADUC.core.command import *

# Database setup
def init_db():
    conn = sqlite3.connect("bot_data.db")
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS welcome_messages (
            user_id INTEGER,
            chat_id INTEGER,
            message_id INTEGER
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS goodbye_messages (
            user_id INTEGER,
            chat_id INTEGER,
            message_id INTEGER
        )
    ''')
    conn.commit()
    conn.close()

# Database functions
def get_welcome(user_id, chat_id):
    conn = sqlite3.connect("bot_data.db")
    c = conn.cursor()
    c.execute("SELECT * FROM welcome_messages WHERE user_id=? AND chat_id=?", (user_id, chat_id))
    result = c.fetchone()
    conn.close()
    return result

def set_welcome(user_id, chat_id, message_id):
    conn = sqlite3.connect("bot_data.db")
    c = conn.cursor()
    c.execute("INSERT OR REPLACE INTO welcome_messages (user_id, chat_id, message_id) VALUES (?, ?, ?)", 
              (user_id, chat_id, message_id))
    conn.commit()
    conn.close()

def get_goodbye(user_id, chat_id):
    conn = sqlite3.connect("bot_data.db")
    c = conn.cursor()
    c.execute("SELECT * FROM goodbye_messages WHERE user_id=? AND chat_id=?", (user_id, chat_id))
    result = c.fetchone()
    conn.close()
    return result

def set_goodbye(user_id, chat_id, message_id):
    conn = sqlite3.connect("bot_data.db")
    c = conn.cursor()
    c.execute("INSERT OR REPLACE INTO goodbye_messages (user_id, chat_id, message_id) VALUES (?, ?, ?)", 
              (user_id, chat_id, message_id))
    conn.commit()
    conn.close()

# Initialize the database
init_db()

# Cache for storing sent messages
GREETINGS_CACHE = {
    "welcome": {},
    "goodbye": {},
}

# Welcome Handler
@app.on_message(filters.new_chat_members & filters.group)
async def welcomehandler(client: Client, message: Message):
    welcome = get_welcome(client.me.id, message.chat.id)
    if not welcome:
        return  # No welcome message set for this chat

    msg = await client.get_messages(LOGGER_ID, welcome[2])
    if not msg:
        return  # Welcome message not found in log group

    # Prepare the text with placeholders replaced
    text = msg.text if msg.text else (msg.caption if msg.caption else None)
    if not text:
        return  # No valid text in the saved message

    # Extract user details
    new_user = message.new_chat_members[0]
    first = new_user.first_name or "User"
    last = new_user.last_name or ""
    fullname = f"{first} {last}".strip()
    mention = new_user.mention or f"[{first}](tg://user?id={new_user.id})"
    username = f"@{new_user.username}" if new_user.username else mention

    # Format the message text
    text = text.format(
        first=first,
        last=last,
        fullname=fullname,
        mention=mention,
        username=username,
        userid=new_user.id,
        chatname=message.chat.title,
        chatid=message.chat.id,
    )

    # Send the welcome message
    sent_msg = await client.send_message(
        chat_id=message.chat.id,
        text=text,
        reply_to_message_id=message.message_id,
    )

    # Cache the message to delete later
    if message.chat.id in GREETINGS_CACHE["welcome"]:
        prev_msg = GREETINGS_CACHE["welcome"][message.chat.id]
        await prev_msg.delete()
    GREETINGS_CACHE["welcome"][message.chat.id] = sent_msg

# Goodbye Handler
@app.on_message(filters.left_chat_member & filters.group)
async def goodbyehandler(client: Client, message: Message):
    goodbye = get_goodbye(client.me.id, message.chat.id)
    if not goodbye:
        return  # No goodbye message set for this chat

    msg = await client.get_messages(LOGGER_ID, goodbye[2])
    if not msg:
        return  # Goodbye message not found in log group

    # Prepare the text with placeholders replaced
    text = msg.text if msg.text else (msg.caption if msg.caption else None)
    if not text:
        return  # No valid text in the saved message

    # Extract user details
    left_user = message.left_chat_member
    first = left_user.first_name or "User"
    last = left_user.last_name or ""
    fullname = f"{first} {last}".strip()
    mention = left_user.mention or f"[{first}](tg://user?id={left_user.id})"
    username = f"@{left_user.username}" if left_user.username else mention

    # Format the message text
    text = text.format(
        first=first,
        last=last,
        fullname=fullname,
        mention=mention,
        username=username,
        userid=left_user.id,
        chatname=message.chat.title,
        chatid=message.chat.id,
    )

    # Send the goodbye message
    sent_msg = await client.send_message(
        chat_id=message.chat.id,
        text=text,
        reply_to_message_id=message.message_id,
    )

    # Cache the message to delete later
    if message.chat.id in GREETINGS_CACHE["goodbye"]:
        prev_msg = GREETINGS_CACHE["goodbye"][message.chat.id]
        await prev_msg.delete()
    GREETINGS_CACHE["goodbye"][message.chat.id] = sent_msg
