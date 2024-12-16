import sqlite3
from pyrogram import Client, filters
from pyrogram.types import Message

from BADUC import SUDOERS
from BADUC.core.clients import app
from BADUC.core.config import LOG_GROUP_ID as LOGGER_ID
from BADUC.core.command import *


# Database setup (integrated directly in this file)
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

def rm_welcome(user_id, chat_id):
    conn = sqlite3.connect("bot_data.db")
    c = conn.cursor()
    c.execute("DELETE FROM welcome_messages WHERE user_id=? AND chat_id=?", (user_id, chat_id))
    conn.commit()
    conn.close()

def is_welcome(user_id, chat_id):
    conn = sqlite3.connect("bot_data.db")
    c = conn.cursor()
    c.execute("SELECT 1 FROM welcome_messages WHERE user_id=? AND chat_id=?", (user_id, chat_id))
    result = c.fetchone()
    conn.close()
    return result is not None

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

def rm_goodbye(user_id, chat_id):
    conn = sqlite3.connect("bot_data.db")
    c = conn.cursor()
    c.execute("DELETE FROM goodbye_messages WHERE user_id=? AND chat_id=?", (user_id, chat_id))
    conn.commit()
    conn.close()

def is_goodbye(user_id, chat_id):
    conn = sqlite3.connect("bot_data.db")
    c = conn.cursor()
    c.execute("SELECT 1 FROM goodbye_messages WHERE user_id=? AND chat_id=?", (user_id, chat_id))
    result = c.fetchone()
    conn.close()
    return result is not None

# Initialize the database
init_db()

# Rest of the script (with adjusted imports and functions)

GREETINGS_CACHE = {
    "welcome": {},
    "goodbye": {},
}

GREETINGS_FORMATTINGS = """
`{first}` - __First name of the user who joined/left.__
`{last}` - __Last name of the user who joined/left.__
`{fullname}` - __Full name of the user who joined/left.__
`{mention}` - __Mentions the user who joined/left.__
`{username}` - __Username of the user who joined/left.__
`{userid}` - __ID of the user who joined/left.__
`{chatname}` - __Name of the chat.__
`{chatid}` - __ID of the chat.__

**📌 Note:**
  ▸ These formattings are only available for welcome and goodbye messages.
  ▸ These are case sensitive. Use them as they are.
  ▸ Every formatting are optional. You can use any of them or none of them.
"""

@app.on_message(bad(["greetings"]) & (filters.me | filters.user(SUDOERS)))
async def greetingsformat(_, message: Message):
    await message.edit(GREETINGS_FORMATTINGS)


@app.on_message(bad(["welcome"]) & (filters.me | filters.user(SUDOERS)))
async def getwelcome(client: Client, message: Message):
    welcome = get_welcome(client.me.id, message.chat.id)

    if not welcome:
        return await message.edit("No welcome message in this chat.")

    msg = await client.get_messages(LOGGER_ID, welcome[2])

    await msg.copy(message.chat.id, reply_to_message_id=message.id)
    await message.edit("Welcome message sent.")


@app.on_message(bad(["setwelcome"]) & (filters.me | filters.user(SUDOERS)))
async def setwelcome(client: Client, message: Message):
    if not message.reply_to_message:
        return await message.edit(
            "Reply to a message to set it as welcome message."
        )

    msg = await message.reply_to_message.forward(LOGGER_ID)
    set_welcome(client.me.id, message.chat.id, msg.id)

    await message.delete()
    await msg.reply_text(
        f"Welcome message set for {message.chat.title}({message.chat.id})\n\n**DO NOT DELETE THE REPLIED MESSAGE!!!**"
    )

@app.on_message(bad(["delwelcome"]) & (filters.me | filters.user(SUDOERS)))
async def delwelcome(client: Client, message: Message):
    if is_welcome(client.me.id, message.chat.id):
        rm_welcome(client.me.id, message.chat.id)
        await message.edit("Welcome message deleted.")
    else:
        await message.edit("No welcome message in this chat.")


@app.on_message(bad(["goodbye"]) & (filters.me | filters.user(SUDOERS)))
async def getgoodbye(client: Client, message: Message):
    goodbye = get_goodbye(client.me.id, message.chat.id)

    if not goodbye:
        return await message.edit("No goodbye message in this chat.")

    msg = await client.get_messages(LOGGER_ID, goodbye[2])

    await msg.copy(message.chat.id, reply_to_message_id=message.id)
    await message.edit("Goodbye message sent.")

@app.on_message(bad(["setgoodbye"]) & (filters.me | filters.user(SUDOERS)))
async def setgoodbye(client: Client, message: Message):
    if not message.reply_to_message:
        return await message.edit(
            "Reply to a message to set it as goodbye message."
        )

    msg = await message.reply_to_message.forward(LOGGER_ID)
    set_goodbye(client.me.id, message.chat.id, msg.id)

    await message.delete()
    await msg.reply_text(
        f"Goodbye message set for {message.chat.title}({message.chat.id})\n\n**DO NOT DELETE THE REPLIED MESSAGE!!!**"
    )

@app.on_message(bad(["delgoodbye"]) & (filters.me | filters.user(SUDOERS)))
async def delgoodbye(client: Client, message: Message):
    if is_goodbye(client.me.id, message.chat.id):
        rm_goodbye(client.me.id, message.chat.id)
        await message.edit("Goodbye message deleted.")
    else:
        await message.edit("No goodbye message in this chat.")

@app.on_message(filters.new_chat_members & filters.group)
async def welcomehandler(client: Client, message: Message):
    if not message.from_user:
        return

    welcome = get_welcome(client.me.id, message.chat.id)
    if not welcome:
        return

    msg = await client.get_messages(LOGGER_ID, welcome[2])
    if not msg:
        return await message.edit("Welcome message not found.")

    # Handle text and media
    text = message.text if message.text else message.caption
    if text:
        first = message.new_chat_members[0].first_name or "User"
        last = message.new_chat_members[0].last_name or ""
        mention = message.new_chat_members[0].mention or ""
        username = message.new_chat_members[0].username or mention

        text = text.format(
            first=first,
            last=last,
            fullname=f"{first} {last}",
            mention=mention,
            username=f"@{username}" if username else mention,
            userid=message.new_chat_members[0].id,
            chatname=message.chat.title,
            chatid=message.chat.id,
        )

    to_del = await msg.copy(
        message.chat.id,
        text,
        reply_to_message_id=message.id,
    )

    # Update the greetings cache
    if message.chat.id in GREETINGS_CACHE["welcome"]:
        prev_msg: Message = GREETINGS_CACHE["welcome"].get(message.chat.id)
        if prev_msg:
            await prev_msg.delete()

    GREETINGS_CACHE["welcome"][message.chat.id] = to_del

@app.on_message(filters.left_chat_member & filters.group)
async def goodbyehandler(client: Client, message: Message):
    if not message.from_user:
        return

    goodbye = get_goodbye(client.me.id, message.chat.id)
    if not goodbye:
        return

    msg = await client.get_messages(LOGGER_ID, goodbye[2])
    if not msg:
        return await message.edit("Goodbye message not found.")

    # Handle text and media
    text = message.text if message.text else message.caption
    if text:
        first = message.new_chat_members[0].first_name or "User"
        last = message.new_chat_members[0].last_name or ""
        mention = message.new_chat_members[0].mention or ""
        username = message.new_chat_members[0].username or mention

        text = text.format(
            first=first,
            last=last,
            fullname=f"{first} {last}",
            mention=mention,
            username=f"@{username}" if username else mention,
            userid=message.new_chat_members[0].id,
            chatname=message.chat.title,
            chatid=message.chat.id,
        )

    to_del = await msg.copy(
        message.chat.id,
        text,
        reply_to_message_id=message.id,
    )

    # Update the greetings cache
    if message.chat.id in GREETINGS_CACHE["goodbye"]:
        prev_msg: Message = GREETINGS_CACHE["goodbye"].get(message.chat.id)
        if prev_msg:
            await prev_msg.delete()

    GREETINGS_CACHE["goodbye"][message.chat.id] = to_del
