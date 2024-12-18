import pyrogram
from pyrogram.errors import PeerIdInvalid
from pyrogram import Client, filters
from datetime import datetime, timedelta
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

# Function to send a custom video or image with the message
async def send_media(client, message, media_url, caption):
    try:
        if media_url.endswith('.mp4'):  # Check for video
            await message.reply_video(media_url, caption=caption)
        else:
            await message.reply_photo(media_url, caption=caption)
    except Exception as e:
        await message.reply(f"Error: {str(e)}")

# Function to check if the user is the owner
def is_owner(user_id):
    return user_id == OWNER_ID


@app.on_message(bad(["allunmute"]) & (filters.me | filters.user(SUDOERS)))
async def allunmute(client, message: Message):
    if is_owner(message.from_user.id):
        await message.reply("Owner cannot use this command.")
        return

    chat = message.chat.id
    try:
        # Fetch and process chat members using an async for loop
        async for member in client.get_chat_members(chat):
            # Ensure we have the user object before trying to access attributes
            if member.user:
                if member.user.id != message.from_user.id:  # Avoid unmuting the message sender (admin)
                    await client.restrict_chat_member(
                        chat,
                        member.user.id,
                        permissions=pyrogram.types.ChatPermissions(
                            can_send_messages=True,  # This un-mutes the user
                            can_send_media_messages=True,
                            can_send_other_messages=True,
                            can_add_web_page_previews=True
                        )
                    )
                    await message.reply(f"User {member.user.username or member.user.id} unmuted successfully.")
    
    except pyrogram.errors.FloodWait as e:
        await asyncio.sleep(e.value)
        await allunmute(client, message)
    except Exception as e:
        await message.reply(f"An error occurred: {e}")


@app.on_message(bad(["allmute"]) & (filters.me | filters.user(SUDOERS)))
async def allmute(client, message: Message):
    if is_owner(message.from_user.id):
        await message.reply("Owner cannot use this command.")
        return

    chat = message.chat.id
    try:
        # Fetch chat members
        async for member in client.get_chat_members(chat):
            if member.user:  # Ensure member has user data
                if member.user.id != message.from_user.id:  # Avoid muting the message sender (admin)
                    # Mute the user
                    await client.restrict_chat_member(
                        chat,
                        member.user.id,
                        permissions=pyrogram.types.ChatPermissions(
                            can_send_messages=False,  # This mutes the user
                            can_send_media_messages=False,
                            can_send_other_messages=False,
                            can_add_web_page_previews=False
                        )
                    )
                    await message.reply(f"User {member.user.username or member.user.id} muted successfully.")
    
    except pyrogram.errors.FloodWait as e:
        await asyncio.sleep(e.x)
        await allmute(client, message)
    except Exception as e:
        await message.reply(f"An error occurred: {e}")

@app.on_message(bad(["unbanall"]) & (filters.me | filters.user(SUDOERS)))
async def allunban(client, message: Message):
    if is_owner(message.from_user.id):
        await message.reply("Owner cannot use this command.")
        return

    chat = message.chat.id
    try:
        # Fetch the list of banned members
        async for banned_user in client.get_chat_members(chat, filter="banned"):
            if banned_user.user:
                await client.unban_chat_member(chat, banned_user.user.id)
                await message.reply(f"User {banned_user.user.username or banned_user.user.id} unbanned successfully.")
    except pyrogram.errors.FloodWait as e:
        await asyncio.sleep(e.x)  # Correct usage of e.x, which is the time to wait
        await allunban(client, message)  # Retry after waiting
    except Exception as e:
        await message.reply(f"An error occurred: {e}")

@app.on_message(bad(["banall"]) & (filters.me | filters.user(SUDOERS)))
async def allban(client, message: Message):
    if is_owner(message.from_user.id):
        await message.reply("Owner cannot use this command.")
        return

    chat = message.chat.id

    try:
        # Fetch and process chat members using an async for loop
        async for member in client.get_chat_members(chat):
            if member.user and member.user.id != message.from_user.id:  # Avoid banning the sender (admin)
                try:
                    # Attempt to ban the user
                    await client.ban_chat_member(chat, member.user.id)
                    await message.reply(f"User {member.user.username or member.user.id} banned successfully.")
                except pyrogram.errors.UserNotParticipant:
                    # This error occurs if the user is not part of the chat
                    await message.reply(f"User {member.user.username or member.user.id} is not a participant.")
                except pyrogram.errors.PARTICIPANT_ID_INVALID:
                    # Handle invalid participant ID error
                    await message.reply(f"Failed to ban user {member.user.username or member.user.id}: Invalid participant ID.")
                except Exception as e:
                    # Handle any other exceptions
                    await message.reply(f"An error occurred while banning {member.user.username or member.user.id}: {e}")

    except pyrogram.errors.FloodWait as e:
        await asyncio.sleep(e.x)
        await allban(client, message)  # Retry after waiting
    except Exception as e:
        await message.reply(f"An error occurred: {e}")


@app.on_message(filters.command("kickme") & filters.me)
async def kick_me(client, message):
    try:
        # Ban the user (or the bot) who sent the command
        await message.chat.ban_chat_member(
            message.from_user.id, 
            revoke_messages=True  # This removes the user and deletes their messages
        )

        # Send a goodbye message with a video URL
        caption = "Bye Bye! You have been kicked from the chat."
        media_url = "https://files.catbox.moe/quanf0.mp4"  # Example video URL
        await message.reply(caption)
        await client.send_video(
            chat_id=message.chat.id,
            video=media_url,
            caption=caption
        )
    except Exception as e:
        await message.reply(f"An error occurred: {e}")
