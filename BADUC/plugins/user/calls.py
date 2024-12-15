from pyrogram import Client, filters
from pyrogram.types import Message

from BADUC import SUDOERS
from BADUC.core.clients import app
from BADUC.core.command import *

# Dictionary to store group settings (enabled or disabled)
enabled_groups = {}

# Command to enable monitoring in a group
@app.on_message(filters.command("vc_notify_on", prefixes=["/"]) & filters.me)
async def enable_notifications(client, message: Message):
    chat_id = message.chat.id
    enabled_groups[chat_id] = True
    await message.reply_text("Voice call notifications enabled for this group.")

# Command to disable monitoring in a group
@app.on_message(filters.command("vc_notify_off", prefixes=["/"]) & filters.me)
async def disable_notifications(client, message: Message):
    chat_id = message.chat.id
    if chat_id in enabled_groups:
        del enabled_groups[chat_id]
    await message.reply_text("Voice call notifications disabled for this group.")

# Monitor voice call join/leave messages
@app.on_message(filters.text & ~filters.private)
async def monitor_voice_chat_events(client, message: Message):
    chat_id = message.chat.id

    # Check if notifications are enabled for this group
    if chat_id not in enabled_groups:
        return

    # Check for voice chat join/leave system messages
    if "joined the group call" in message.text:
        user_name = message.from_user.first_name or "Unknown"
        user_id = message.from_user.id
        await message.reply_text(f"🔊 {user_name} joined the voice chat. [User ID: {user_id}]")

    elif "left the group call" in message.text:
        user_name = message.from_user.first_name or "Unknown"
        user_id = message.from_user.id
        await message.reply_text(f"🔇 {user_name} left the voice chat. [User ID: {user_id}]")
