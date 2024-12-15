from pyrogram import Client, filters
from pyrogram.types import Message

from BADUC import SUDOERS
from BADUC.core.clients import app
from BADUC.core.command import *

# Dictionary to store group settings (enabled or disabled)
enabled_groups = {}

# Command to enable monitoring in a group
@app.on_message(bad(["vcnoti_on"]) & (filters.me | filters.user(SUDOERS)))
async def enable_notifications(client, message: Message):
    chat_id = message.chat.id
    enabled_groups[chat_id] = True
    await message.reply_text("Voice call notifications enabled for this group.")

# Command to disable monitoring in a group
@app.on_message(bad(["vcnoti_of"]) & (filters.me | filters.user(SUDOERS)))
async def disable_notifications(client, message: Message):
    chat_id = message.chat.id
    if chat_id in enabled_groups:
        del enabled_groups[chat_id]
    await message.reply_text("Voice call notifications disabled for this group.")

# Monitor voice call joins
@app.on_chat_member_updated()
async def monitor_voice_calls(client, chat_member_updated):
    chat_id = chat_member_updated.chat.id

    # Check if notifications are enabled for this group
    if chat_id not in enabled_groups:
        return

    # Get old and new member statuses
    old_status = chat_member_updated.old_chat_member
    new_status = chat_member_updated.new_chat_member

    # Check if the user joined or left the voice chat
    if old_status.is_member and not new_status.is_member:
        # User left the voice chat
        user_name = new_status.user.first_name or "Unknown"
        await client.send_message(
            chat_id,
            f"{user_name} has left the voice chat. [User ID: {new_status.user.id}]"
        )
    elif not old_status.is_member and new_status.is_member:
        # User joined the voice chat
        user_name = new_status.user.first_name or "Unknown"
        await client.send_message(
            chat_id,
            f"{user_name} has joined the voice chat. [User ID: {new_status.user.id}]"
        )
      
