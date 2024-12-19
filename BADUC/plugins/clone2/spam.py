import asyncio
from pyrogram import filters
from pyrogram import Client
from pyrogram.types import Message

from BADUC.core.config import LOG_GROUP_ID
from BADUC.plugins.bot.clone3 import get_bot_owner  # Assuming get_bot_owner is available

import random
import time
import os
import json

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
            await Client.copy_message(
                chat_id, chat_id, copy_id, reply_to_message_id=reply_to
            )
        else:
            await Client.send_message(
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
    await Client.send_message(
        LOG_GROUP_ID,
        f"**Spam Task Completed**\n\n**Type:** {spam_type}\n**Chat ID:** `{chat_id}`\n**Spam Count:** `{count}`",
    )


async def check_owner(Client: Client, message: Message):
    bot_info = await Client.get_me()
    bot_id = bot_info.id
    user_id = message.from_user.id
    
    # Authorization check
    owner_id = await get_bot_owner(bot_id)
    if owner_id != user_id:
        await message.reply_text("❌ You're not authorized to use this bot.")
        return False
    return True


@Client.on_message(filters.command("spam"))
async def spamMessage(Client: Client, message: Message):
    # Authorization check
    if not await check_owner(Client, message):
        return

    if len(message.command) < 3:
        return await Client.delete(message, "Give me something to spam.")

    reply_to = message.reply_to_message.id if message.reply_to_message else None
    try:
        count = int(message.command[1])
    except ValueError:
        return await Client.delete(message, "Give me a valid number to spam.")

    to_spam = message.text.split(" ", 2)[2].strip()
    event = asyncio.Event()
    task = asyncio.create_task(
        spam_text(Client, message.chat.id, to_spam, count, reply_to, None, None, event)
    )

    if spamTask.get(message.chat.id, None):
        spamTask[message.chat.id].append(event)
    else:
        spamTask[message.chat.id] = [event]

    # Log spam initiation to the Logger Group
    await Client.send_message(
        LOG_GROUP_ID,
        f"**Spam Task Started**\n\n**Type:** Text Spam\n**Chat ID:** `{message.chat.id}`\n**Spam Count:** `{count}`\n**Message:** `{to_spam}`",
    )

    await message.delete()
    await task


@Client.on_message(filters.command("mspam"))
async def mediaSpam(Client: Client, message: Message):
    # Authorization check
    if not await check_owner(Client, message):
        return

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
        spam_text(Client, message.chat.id, None, count, None, None, copy_id, event)
    )

    if spamTask.get(message.chat.id, None):
        spamTask[message.chat.id].append(event)
    else:
        spamTask[message.chat.id] = [event]

    # Log spam initiation to the Logger Group
    await Client.send_message(
        LOG_GROUP_ID,
        f"**Spam Task Started**\n\n**Type:** Media Spam\n**Chat ID:** `{message.chat.id}`\n**Spam Count:** `{count}`",
    )

    await message.delete()
    await task


@Client.on_message(filters.command("stopspam"))
async def stopSpam(_, message: Message):
    # Authorization check
    if not await check_owner(_, message):
        return

    chat_id = message.chat.id

    if not spamTask.get(chat_id, None):
        return await Client.delete(message, "No spam task running for this chat.")

    for event in spamTask[chat_id]:
        event.set()

    chat_name = message.chat.title or message.chat.first_name
    del spamTask[chat_id]

    # Log spam task termination to the Logger Group
    await Client.send_message(
        LOG_GROUP_ID,
        f"**Spam Task Stopped**\n\n**Chat ID:** `{chat_id}`\n**Chat Name:** `{chat_name}`",
    )

    await Client.delete(message, f"Spam task stopped for {chat_name}.")
