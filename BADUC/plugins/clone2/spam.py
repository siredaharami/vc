import asyncio
from pyrogram import filters
from pyrogram import Client
from pyrogram.types import Message

from BADUC.core.config import LOG_GROUP_ID

import random
import time
import os
import json

# Load clone data
CLONE_DATA_FILE = "clone_data.json"

def load_clone_data():
    if os.path.exists(CLONE_DATA_FILE):
        with open(CLONE_DATA_FILE, "r") as file:
            return json.load(file)
    return {}

def is_cloned_user(user_id):
    """Check if the user is a cloned bot owner."""
    clone_data = load_clone_data()
    for _, details in clone_data.items():
        if details.get("owner_id") == user_id:
            return True
    return False
    

# Decorator for commands restricted to cloned bot owners
def cloned_user_only(func):
    async def wrapper(client: Client, message: Message):
        user_id = message.from_user.id
        if not is_cloned_user(user_id):
            await message.reply("You are not authorized to use this command!")
            return
        return await func(client, message)
    return wrapper
    
    
spamTask = {}

async def spam_text(
    Client: Client,
    chat_id: int,
    to_spam: str,
    count: int,
    reply_to: int,
    delay: float,
    copy_id: int,
    event: asyncio.Event,
):
    for _ in range(count):
        if event.is_set():
            break

        if copy_id:
            await bot.copy_message(
                chat_id, chat_id, copy_id, reply_to_message_id=reply_to
            )
        else:
            await bot.send_message(
                chat_id,
                to_spam,
                disable_web_page_preview=True,
                reply_to_message_id=reply_to,
            )
        if delay:
            await asyncio.sleep(delay)

    try:
        event.set()
        task = spamTask.get(chat_id, None)
        if task:
            task.remove(event)
    except:
        pass

    # Log spam details to the Logger Group
    spam_type = "Media Spam" if copy_id else "Text Spam"
    await bot.send_message(
        LOG_GROUP_ID,
        f"**Spam Task Completed**\n\n**Type:** {spam_type}\n**Chat ID:** `{chat_id}`\n**Spam Count:** `{count}`",
    )


@Client.on_message(filters.command("spam"))
@cloned_user_only
async def spamMessage(bot: bot, message: Message):
    if len(message.command) < 3:
        return await bot.delete(message, "Give me something to spam.")

    reply_to = message.reply_to_message.id if message.reply_to_message else None
    try:
        count = int(message.command[1])
    except ValueError:
        return await bot.delete(message, "Give me a valid number to spam.")

    to_spam = message.text.split(" ", 2)[2].strip()
    event = asyncio.Event()
    task = asyncio.create_task(
        spam_text(bot, message.chat.id, to_spam, count, reply_to, None, None, event)
    )

    if spamTask.get(message.chat.id, None):
        spamTask[message.chat.id].append(event)
    else:
        spamTask[message.chat.id] = [event]

    # Log spam initiation to the Logger Group
    await bot.send_message(
        LOG_GROUP_ID,
        f"**Spam Task Started**\n\n**Type:** Text Spam\n**Chat ID:** `{message.chat.id}`\n**Spam Count:** `{count}`\n**Message:** `{to_spam}`",
    )

    await message.delete()
    await task


@Client.on_message(filters.command("mspam"))
@cloned_user_only
async def mediaSpam(bot: bot, message: Message):
    if not message.reply_to_message:
        return await message.delete()

    if len(message.command) < 2:
        return await message.delete()

    try:
        count = int(message.command[1])
    except ValueError:
        await message.delete()
        return

    copy_id = message.reply_to_message.id
    event = asyncio.Event()
    task = asyncio.create_task(
        spam_text(bot, message.chat.id, None, count, None, None, copy_id, event)
    )

    if spamTask.get(message.chat.id, None):
        spamTask[message.chat.id].append(event)
    else:
        spamTask[message.chat.id] = [event]

    # Log spam initiation to the Logger Group
    await bot.send_message(
        LOG_GROUP_ID,
        f"**Spam Task Started**\n\n**Type:** Media Spam\n**Chat ID:** `{message.chat.id}`\n**Spam Count:** `{count}`",
    )

    await message.delete()
    await task


@Client.on_message(filters.command("stopspam"))
@cloned_user_only
async def stopSpam(_, message: Message):
    chat_id = message.chat.id

    if not spamTask.get(chat_id, None):
        return await bot.delete(message, "No spam task running for this chat.")

    for event in spamTask[chat_id]:
        event.set()

    chat_name = message.chat.title or message.chat.first_name
    del spamTask[chat_id]

    # Log spam task termination to the Logger Group
    await bot.send_message(
        LOG_GROUP_ID,
        f"**Spam Task Stopped**\n\n**Chat ID:** `{chat_id}`\n**Chat Name:** `{chat_name}`",
    )

    await bot.delete(message, f"Spam task stopped for {chat_name}.")
