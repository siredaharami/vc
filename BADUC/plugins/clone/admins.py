import pyrogram
from pyrogram import Client, filters
from datetime import datetime, timedelta
from pyrogram.errors import ChatAdminRequired
from pyrogram.types import ChatPermissions, ChatPrivileges, Message
from pyrogram.types import Message
from BADUC.database.misc import extract_user
from pyrogram.errors import FloodWait
import asyncio

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
    return user_id == SUDOERS

# 1. ban
@Client.on_message(bad(["ban"]) & (filters.me | filters.user(SUDOERS)))
async def ban_user(client, message: Message):
    if is_owner(message.from_user.id):
        await message.reply("Owner cannot use this command.")
        return
    if message.reply_to_message:
        try:
            user_to_ban = message.reply_to_message.from_user
            user_banning = message.from_user

            # Check if the user being banned is an admin
            if await is_admin(client, message.chat.id, user_to_ban.id):
                await message.reply(f"Aap admin ko nahi bana sakte, {user_to_ban.first_name}. (You cannot ban an admin.)", quote=True)
                return
            
            # Ban the user
            await client.ban_chat_member(message.chat.id, user_to_ban.id)

            # Prepare message with both usernames
            caption = (
                f"User @{user_to_ban.username} ({user_to_ban.first_name}) "
                f"has been banned by @{user_banning.username} ({user_banning.first_name})."
            )
            media_url = "https://files.catbox.moe/6yko4k.mp4"  # Video URL
            await send_media(client, message, media_url, caption)
        except FloodWait as e:
            await asyncio.sleep(e.x)
            await ban_user(client, message)
    else:
        await message.reply("Reply to a message to ban user.")

# 2. unban
@Client.on_message(bad(["unban"]) & (filters.me | filters.user(SUDOERS)))
async def unban_user(client, message: Message):
    if is_owner(message.from_user.id):
        await message.reply("Owner cannot use this command.")
        return
    if message.reply_to_message:
        try:
            user_to_unban = message.reply_to_message.from_user
            user_unbanning = message.from_user

            if await is_admin(client, message.chat.id, user_to_unban.id):
                await message.reply(f"Aap admin ko nahi unban kar sakte, {user_to_unban.first_name}. (You cannot unban an admin.)", quote=True)
                return

            await client.unban_chat_member(message.chat.id, user_to_unban.id)  # Correct method for unbanning
            caption = (
                f"User @{user_to_unban.username} ({user_to_unban.first_name}) "
                f"has been unbanned by @{user_unbanning.username} ({user_unbanning.first_name})."
            )
            media_url = "https://files.catbox.moe/rudmdy.mp4"  # Video URL
            await send_media(client, message, media_url, caption)
        except FloodWait as e:
            await asyncio.sleep(e.x)
            await unban_user(client, message)
    else:
        await message.reply("Reply to a message to unban user.")

# 3. mute
@Client.on_message(bad(["mute"]) & (filters.me | filters.user(SUDOERS)))
async def mute_user(client, message: Message):
    if is_owner(message.from_user.id):
        await message.reply("Owner cannot use this command.")
        return
    if message.reply_to_message:
        try:
            user_to_mute = message.reply_to_message.from_user
            user_muting = message.from_user

            if await is_admin(client, message.chat.id, user_to_mute.id):
                await message.reply(f"Aap admin ko nahi mute kar sakte, {user_to_mute.first_name}. (You cannot mute an admin.)", quote=True)
                return

            # Use restrict_chat_member to mute the user
            await client.restrict_chat_member(
                message.chat.id,
                user_to_mute.id,
                permissions=pyrogram.types.ChatPermissions(can_send_messages=False)  # Restrict the ability to send messages
            )
            caption = (
                f"User @{user_to_mute.username} ({user_to_mute.first_name}) "
                f"has been muted by @{user_muting.username} ({user_muting.first_name})."
            )
            media_url = "https://files.catbox.moe/quanf0.mp4"  # Video URL
            await send_media(client, message, media_url, caption)
        except FloodWait as e:
            await asyncio.sleep(e.x)
            await mute_user(client, message)
    else:
        await message.reply("Reply to a message to mute user.")
# 4. unmute
@Client.on_message(bad(["unmute"]) & (filters.me | filters.user(SUDOERS)))
async def unmute_user(client, message: Message):
    if is_owner(message.from_user.id):
        await message.reply("Owner cannot use this command.")
        return
    if message.reply_to_message:
        try:
            user_to_unmute = message.reply_to_message.from_user
            user_unmuting = message.from_user

            if await is_admin(client, message.chat.id, user_to_unmute.id):
                await message.reply(f"Aap admin ko nahi unmute kar sakte, {user_to_unmute.first_name}. (You cannot unmute an admin.)", quote=True)
                return

            # Use restrict_chat_member to remove the mute restrictions
            await client.restrict_chat_member(
                message.chat.id,
                user_to_unmute.id,
                permissions=pyrogram.types.ChatPermissions(can_send_messages=True)  # Allow the user to send messages again
            )
            caption = (
                f"User @{user_to_unmute.username} ({user_to_unmute.first_name}) "
                f"has been unmuted by @{user_unmuting.username} ({user_unmuting.first_name})."
            )
            media_url = "https://files.catbox.moe/quanf0.mp4"  # Video URL (optional)
            await send_media(client, message, media_url, caption)
        except FloodWait as e:
            await asyncio.sleep(e.x)
            await unmute_user(client, message)
    else:
        await message.reply("Reply to a message to unmute user.")
        

# 6. allban (Updated version with no text/GIF)

@Client.on_message(bad(["kick"]) & (filters.me | filters.user(SUDOERS)))
async def kick_user(client, message: Message):
    if is_owner(message.from_user.id):
        await message.reply("Owner cannot use this command.")
        return

    # Check if the message is a reply
    if not message.reply_to_message:
        await message.reply("Please reply to the message of the user you want to kick.")
        return

    user_to_kick = message.reply_to_message.from_user

    try:
        # Ban the user
        await client.ban_chat_member(message.chat.id, user_to_kick.id)

        # Optionally delete the user's messages
        async for msg in client.search_messages(
            chat_id=message.chat.id, 
            from_user=user_to_kick.id
        ):
            await client.delete_messages(chat_id=message.chat.id, message_ids=msg.id)

        # Video URL
        video_url = "https://files.catbox.moe/zefegl.mp4"  # Replace with your desired video URL

        # Send video with the kick message
        await client.send_video(
            chat_id=message.chat.id,
            video=video_url,
            caption=f"User {user_to_kick.username or user_to_kick.id} has been kicked successfully."
        )

    except pyrogram.errors.ChatAdminRequired:
        await message.reply("I need to be an admin with the proper permissions to perform this action.")
    except Exception as e:
        await message.reply(f"An error occurred: {e}")
        


# 11. Promote (Updated with both usernames and video link)
@Client.on_message(bad(["promote"]) & (filters.me | filters.user(SUDOERS)))
async def promote_user(client, message: Message):
    if is_owner(message.from_user.id):
        await message.reply("Owner cannot use this command.")
        return
    if message.reply_to_message:
        try:
            user_to_promote = message.reply_to_message.from_user
            user_promoting = message.from_user

            if await is_admin(client, message.chat.id, user_to_promote.id):
                await message.reply(f"Aap admin ko nahi promote kar sakte, {user_to_promote.first_name}. (You cannot promote an admin.)", quote=True)
                return

            await client.promote_chat_member(message.chat.id, user_to_promote.id)
            caption = (
                f"User @{user_to_promote.username} ({user_to_promote.first_name}) "
                f"has been promoted to admin by @{user_promoting.username} ({user_promoting.first_name})."
            )
            media_url = "https://files.catbox.moe/zefegl.mp4"  # Replace with actual video link
            await send_media(client, message, media_url, caption)
        except FloodWait as e:
            await asyncio.sleep(e.x)
            await promote_user(client, message)
    else:
        await message.reply("Reply to a message to promote user.")


@Client.on_message(bad(["fullpromote"]) & (filters.me | filters.user(SUDOERS)))
async def promotte(client: Client, message: Message):
    user_id = await extract_user(message)
    umention = (await client.get_users(user_id)).mention
    rd = await message.edit_text("`Processing...`")
    if not user_id:
        return await rd.edit("I can't find that user.")
    bot = (await client.get_chat_member(message.chat.id, client.me.id)).privileges
    if not bot.can_promote_members:
        return await rd.edit("I don't have enough permissions")
    if message.command[0][0] == "f":
        await message.chat.promote_member(
            user_id,
            privileges=ChatPrivileges(
                can_manage_chat=True,
                can_delete_messages=True,
                can_manage_video_chats=True,
                can_restrict_members=True,
                can_change_info=True,
                can_invite_users=True,
                can_pin_messages=True,
                can_promote_members=True,
            ),
        )
        return await rd.edit(f"Fully Promoted! {umention}")

    await message.chat.promote_member(
        user_id,
        privileges=ChatPrivileges(
            can_manage_chat=True,
            can_delete_messages=True,
            can_manage_video_chats=True,
            can_restrict_members=True,
            can_change_info=True,
            can_invite_users=True,
            can_pin_messages=True,
            can_promote_members=False,
        ),
    )
    await rd.edit(f"Promoted! {umention}")


@Client.on_message(bad(["demote"]) & (filters.me | filters.user(SUDOERS)))
async def demote(client: Client, message: Message):
    user_id = await extract_user(message)
    rd = await message.edit_text("`Processing...`")
    if not user_id:
        return await rd.edit("I can't find that user.")
    if user_id == client.me.id:
        return await rd.edit("I can't demote myself.")
    await message.chat.promote_member(
        user_id,
        privileges=ChatPrivileges(
            can_manage_chat=False,
            can_delete_messages=False,
            can_manage_video_chats=False,
            can_restrict_members=False,
            can_change_info=False,
            can_invite_users=False,
            can_pin_messages=False,
            can_promote_members=False,
        ),
    )
    umention = (await client.get_users(user_id)).mention
    await rd.edit(f"Demoted! {umention}")

  
