from random import choice
from pyrogram import filters, Client
from pyrogram.types import Message
from BADUC.plugins.bot.clone3 import get_bot_owner
import asyncio
import random

# Import additional constants or data if required
from BADUC import SUDOERS as SUDO_USER
from BADUC.database.data import *

ACTIVATE_RLIST = []

# Function to check if the user is authorized
async def is_authorized(client, message):
    bot_info = await client.get_me()  # Retrieve current bot's details
    bot_id = bot_info.id  # Get the current bot's ID
    user_id = message.from_user.id  # Get the user's ID

    owner_id = await get_bot_owner(bot_id)
    if owner_id != user_id:
        await message.reply_text("❌ You're not authorized to use this bot.")
        return False
    return True

# Raid Handler Template
async def handle_raid(client, message, raid_type, raid_list):
    if not await is_authorized(client, message):
        return  # If not authorized, exit the function

    args = "".join(message.text.split(maxsplit=1)[1:]).split(" ", 2)
    if len(args) == 2:
        try:
            counts = int(args[0])
            username = args[1]
        except ValueError:
            await message.reply_text(f"Invalid format. Use: /{raid_type} count username or reply.")
            return
    elif message.reply_to_message:
        try:
            counts = int(args[0])
            username = message.reply_to_message.from_user.id
        except ValueError:
            await message.reply_text(f"Invalid format. Use: /{raid_type} count username or reply.")
            return
    else:
        await message.reply_text(f"Usage: /{raid_type} count username or reply.")
        return

    try:
        user = await client.get_users(username)
    except Exception:
        await message.reply_text("**Error:** User not found or may be deleted!")
        return

    if int(message.chat.id) in GROUP:
        await message.reply_text("**Sorry !! I can't Spam Here.**")
        return
    if int(user.id) in VERIFIED_USERS:
        await message.reply_text("I can't raid my developer.")
        return
    if int(user.id) in SUDO_USER:
        await message.reply_text("This guy is a sudo user.")
        return

    mention = user.mention
    for _ in range(counts):
        response = f"{mention} {choice(raid_list)}"
        await client.send_message(message.chat.id, response)
        await asyncio.sleep(0.3)

# PBIRAID
@Client.on_message(filters.command("praid"))
async def pbiraid(client: Client, message: Message):
    await handle_raid(client, message, "praid", PBIRAID)

# OneWord RAID
@Client.on_message(filters.command("oraid"))
async def oneword_raid(client: Client, message: Message):
    await handle_raid(client, message, "oraid", OneWord)

# HIRAID
@Client.on_message(filters.command("hraid"))
async def hiraid(client: Client, message: Message):
    await handle_raid(client, message, "hraid", HIRAID)
