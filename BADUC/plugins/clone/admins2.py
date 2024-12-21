import pyrogram
from pyrogram.errors import PeerIdInvalid
from pyrogram import Client, filters
from datetime import datetime, timedelta
from pyrogram.types import Message
from pyrogram.errors import FloodWait
import asyncio

from BADUC.core.config import OWNER_ID  # Import OWNER_ID from config.py
from BADUC import SUDOERS
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

@Client.on_message(filters.command(["allmute"]) & (filters.me | filters.user(SUDOERS)))
async def allmute(client, message: Message):
    if is_owner(message.from_user.id):
        await message.reply("Owner cannot use this command.")
        return

    chat = message.chat.id
    try:
        # Check if the bot has admin privileges and can restrict members
        bot_member = await client.get_chat_member(chat, client.me.id)
        if bot_member.status != "administrator" or not bot_member.can_restrict_members:
            await message.reply("Bot does not have permission to mute members.")
            return

        # Fetch and process chat members using an async for loop
        async for member in client.get_chat_members(chat):
            if member.user.id != message.from_user.id:  # Avoid muting the message sender (admin)
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
        await asyncio.sleep(e.value)
        await allmute(client, message)
    except Exception as e:
        await message.reply(f"An error occurred: {e}")

@Client.on_message(filters.command(["allunmute"]) & (filters.me | filters.user(SUDOERS)))
async def allunmute(client, message: Message):
    if is_owner(message.from_user.id):
        await message.reply("Owner cannot use this command.")
        return

    chat = message.chat.id
    try:
        # Check if the bot has admin privileges and can restrict members
        bot_member = await client.get_chat_member(chat, client.me.id)
        if bot_member.status != "administrator" or not bot_member.can_restrict_members:
            await message.reply("Bot does not have permission to unmute members.")
            return

        # Fetch and process chat members using an async for loop
        async for member in client.get_chat_members(chat):
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

# Command to unban all members
@Client.on_message(filters.command(["unbanall"]) & (filters.me | filters.user(SUDOERS)))
async def unban_all(client, message):
    # Check if the user is an admin
    chat_id = message.chat.id
    user_id = message.from_user.id
    member = await client.get_chat_member(chat_id, user_id)

    if member.status not in ["administrator", "creator"]:
        await message.reply("You need to be an admin to use this command.")
        return

    try:
        # Get all banned members
        banned_members = await client.get_chat_members(chat_id, filter="banned")
        
        if not banned_members:
            await message.reply("There are no banned members.")
            return
        
        # Unban each member
        for banned_user in banned_members:
            try:
                await client.unban_chat_member(chat_id, banned_user.user.id)
                print(f"Unbanned user: {banned_user.user.username or banned_user.user.id}")
                await message.reply(f"Unbanned {banned_user.user.username or banned_user.user.id}")
            except PeerIdInvalid:
                print(f"Could not unban user {banned_user.user.id}")
        
        await message.reply("All banned members have been unbanned.")
    except Exception as e:
        await message.reply(f"An error occurred: {e}")
        print(f"Error: {e}")

# Command to ban all members
@Client.on_message(filters.command(["banall"]) & (filters.me | filters.user(SUDOERS)))
async def ban_all(client, message):
    # Check if the user is an admin
    chat_id = message.chat.id
    user_id = message.from_user.id
    member = await client.get_chat_member(chat_id, user_id)

    if member.status not in ["administrator", "creator"]:
        await message.reply("You need to be an admin to use this command.")
        return

    try:
        # Get all members in the group
        members = client.get_chat_members(chat_id)
        
        # Exclude the bot and admins
        members_to_ban = []
        async for m in members:
            if m.user.id != client.me.id and m.status not in ["administrator", "creator"]:
                members_to_ban.append(m)

        if not members_to_ban:
            await message.reply("There are no members to ban (only admins or the bot).")
            return
        
        # Ban each member
        for member in members_to_ban:
            try:
                await client.ban_chat_member(chat_id, member.user.id)
                print(f"Banned user: {member.user.username or member.user.id}")
                await message.reply(f"Banned {member.user.username or member.user.id}")
            except PeerIdInvalid:
                print(f"Could not ban user {member.user.id}")
        
        await message.reply("All members (except admins and the bot) have been banned.")
    except Exception as e:
        await message.reply(f"An error occurred: {e}")
        print(f"Error: {e}")

# Command to make the user leave the group
@Client.on_message(filters.command(["kickme"]) & (filters.me | filters.user(SUDOERS)))
async def kick_me(client, message):
    # Check if the command was issued in a group
    if not message.chat:
        await message.reply("This command can only be used in a group.")
        return

    # Ensure the user is part of the group
    if message.from_user.id not in [member.user.id for member in await client.get_chat_members(message.chat.id)]:
        await message.reply("You are not a member of this group.")
        return

    # Send a confirmation message before leaving the group
    await message.reply("You will be kicked and leave the group now.")
    
    try:
        # Kick the user from the group (this removes them from the group)
        await client.kick_chat_member(message.chat.id, message.from_user.id)
        print(f"User {message.from_user.username or message.from_user.id} has been kicked and will leave the group.")
    except PeerIdInvalid:
        await message.reply("Failed to kick you from the group.")
        print(f"Failed to kick user {message.from_user.id}")
          
