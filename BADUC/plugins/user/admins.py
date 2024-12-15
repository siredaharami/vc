from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.errors import FloodWait
import asyncio
from BADUC.core.config import OWNER_ID  # Import OWNER_ID from config.py

from BADUC import SUDOERS
from BADUC.core.clients import app
from BADUC.core.command import *

# Function to check if the user is an admin
async def is_admin(client, chat_id, user_id):
    chat_member = await client.get_chat_member(chat_id, user_id)
    return chat_member.status in ["administrator", "creator"]

# Function to send a custom GIF or image with the message
async def send_media(client, message, media_url, caption):
    try:
        if media_url.endswith('.gif'):
            await message.reply_animation(media_url, caption=caption)
        else:
            await message.reply_photo(media_url, caption=caption)
    except Exception as e:
        await message.reply(f"Error: {str(e)}")

# Function to check if the user is the owner
def is_owner(user_id):
    return user_id == OWNER_ID

# 1. ban
@app.on_message(bad(["ban"]) & (filters.me | filters.user(SUDOERS)))
async def ban_user(client, message: Message):
    if is_owner(message.from_user.id):
        await message.reply("Owner cannot use this command.")
        return
    if message.reply_to_message:
        try:
            user_to_ban = message.reply_to_message.from_user
            if await is_admin(client, message.chat.id, user_to_ban.id):
                await message.reply(f"Aap admin ko nahi bana sakte, {user_to_ban.first_name}. (You cannot ban an admin.)", quote=True)
                return
            await message.reply_to_message.ban()
            caption = f"User {user_to_ban.first_name} has been banned."
            media_url = "https://files.catbox.moe/43eyt0.mp4"
            await send_media(client, message, media_url, caption)
        except FloodWait as e:
            await asyncio.sleep(e.x)
            await ban_user(client, message)
    else:
        await message.reply("Reply to a message to ban user.")
