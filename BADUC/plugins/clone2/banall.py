from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, CallbackQuery
from pyrogram.enums import ChatMemberStatus, ParseMode, ChatType
import asyncio
import os
from os import getenv
import traceback
from pyrogram.types import Message
from unidecode import unidecode
import random
import time
import requests
from BADUC.plugins.bot.clone3 import get_bot_owner  # Import the function to check bot owner

# Placeholder for is_authorized function
async def is_authorized(client, message):
    # Assuming you want to check if the user is the bot owner
    user_id = message.from_user.id
    bot_info = await client.get_me()  # Retrieve bot info
    bot_id = bot_info.id  # Get the bot ID
    owner_id = await get_bot_owner(bot_id)  # Fetch the owner ID
    
    return user_id == owner_id  # Returns True if the user is authorized

# Ban All Command with Authorization Check
@Client.on_message(filters.command(["banall"], prefixes=[".", "/", "!"]) & filters.group)
async def ban_all(client, msg):
    chat_id = msg.chat.id
    user_id = msg.from_user.id

    # Check bot details and owner
    bot_info = await client.get_me()  # Retrieve current bot's details
    bot_id = bot_info.id  # Get the current bot's ID
    owner_id = await get_bot_owner(bot_id)  # Fetch the owner ID

    # If the user is not authorized, deny the command
    if not await is_authorized(client, msg):
        await msg.reply_text("❌ You're not authorized to use this bot.")
        return

    LOL = await msg.reply_text("🚨 Initiating ban process...")
    bot = await client.get_chat_member(chat_id, bot_id)
    bot_permission = bot.privileges and bot.privileges.can_restrict_members

    if bot_permission:
        x = 0
        async for member in client.get_chat_members(chat_id):
            try:
                await client.ban_chat_member(chat_id, member.user.id)
                x += 1
                await LOL.edit_text(f"✫ Banned Users: {x} ✫")
            except Exception as e:
                print(f"Error banning user {member.user.id}: {e}")
    else:
        await msg.reply_text("❌ I don't have the permission to restrict users.")
