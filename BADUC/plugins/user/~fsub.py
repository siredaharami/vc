from BADUC import SUDOERS
from BADUC.core.clients import app
from BADUC.core.command import *
from BADUC.core.config import MONGO_DB_URL

from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pymongo import MongoClient
import asyncio
from pyrogram.enums import ChatMembersFilter
from pyrogram.errors import (
    ChatAdminRequired,
    UserNotParticipant,
)

# MongoDB Setup
fsubdb = MongoClient(MONGO_DB_URL)
forcesub_collection = fsubdb.status_db.status

@app.on_message(filters.command(["fsub", "forcesub"]))
async def set_forcesub(client: Client, message: Message):
    user_id = message.from_user.id

    # Check if the user is a SUDO user
    if user_id not in SUDOERS:
        return await message.reply_photo(
            photo="https://envs.sh/Tn_.jpg",
            caption="🚫 **Only authorized SUDO users can use this command.**"
        )

    chat_id = message.chat.id

    # Disable Force Subscription
    if len(message.command) == 2 and message.command[1].lower() in ["off", "disable"]:
        forcesub_collection.delete_one({"chat_id": chat_id})
        return await message.reply_photo(
            photo="https://envs.sh/Tn_.jpg",
            caption="✅ **Force subscription has been disabled for this group.**"
        )

    # Enable Force Subscription
    if len(message.command) != 2:
        return await message.reply_photo(
            photo="https://envs.sh/Tn_.jpg",
            caption="**Usage:**\n`/fsub <channel username or ID>`\nOR\n`/fsub off` to disable"
        )

    channel_input = message.command[1]

    try:
        # Get Channel Info
        channel_info = await client.get_chat(channel_input)
        channel_id = channel_info.id
        channel_title = channel_info.title
        channel_username = channel_info.username if channel_info.username else None

        # Check if user bot is admin in the channel
        bot_is_admin = False
        async for admin in client.get_chat_members(channel_id, filter=ChatMembersFilter.ADMINISTRATORS):
            if admin.user.id == user_id:  # User bot's own ID
                bot_is_admin = True
                break

        if not bot_is_admin:
            return await message.reply_photo(
                photo="https://envs.sh/Tn_.jpg",
                caption="🚫 **I am not an admin in the specified channel.**\n\n"
                        "Please make me an admin with 'Invite New Members' permission."
            )

        # Save Force Subscription Settings
        forcesub_collection.update_one(
            {"chat_id": chat_id},
            {"$set": {"channel_id": channel_id, "channel_username": channel_username}},
            upsert=True
        )

        await message.reply_photo(
            photo="https://envs.sh/Tn_.jpg",
            caption=(
                f"🎉 **Force subscription enabled successfully!**\n\n"
                f"📌 **Channel:** `{channel_title}`\n"
                f"🆔 **Channel ID:** `{channel_id}`\n"
                f"🔗 **Channel Link:** [Click Here](https://t.me/{channel_username})\n"
                f"👤 **Set by:** {message.from_user.mention}"
            )
        )
    except Exception as e:
        await message.reply_photo(
            photo="https://envs.sh/Tn_.jpg",
            caption=f"🚫 **Error:**\n{str(e)}"
        )


async def check_forcesub(client: Client, message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id

    # Check Force Subscription Settings
    forcesub_data = forcesub_collection.find_one({"chat_id": chat_id})
    if not forcesub_data:
        return True  # No force subscription set

    channel_id = forcesub_data["channel_id"]
    channel_username = forcesub_data.get("channel_username")

    try:
        # Check if the user is a member of the channel
        user_member = await client.get_chat_member(channel_id, user_id)
        if user_member:
            return True
    except UserNotParticipant:
        # If user is not a participant, delete their message
        await message.delete()
        channel_link = f"https://t.me/{channel_username}" if channel_username else None
        return await message.reply_photo(
            photo="https://envs.sh/Tn_.jpg",
            caption=(
                f"👋 **Hello {message.from_user.mention},**\n\n"
                f"You need to join the [Channel]({channel_link}) to send messages in this group."
            ),
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("Join Channel", url=channel_link)]]
            )
        )
    except ChatAdminRequired:
        forcesub_collection.delete_one({"chat_id": chat_id})
        await message.reply_photo(
            photo="https://envs.sh/Tn_.jpg",
            caption="🚫 **I am no longer an admin in the channel.**\n"
                    "Force subscription has been disabled."
        )
        return False

    return True


@app.on_message(filters.group)
async def enforce_forcesub(client: Client, message: Message):
    if not await check_forcesub(client, message):
        return
      
