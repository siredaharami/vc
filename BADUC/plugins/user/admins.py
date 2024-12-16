import pyrogram
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

# 1. ban
@app.on_message(bad(["ban"]) & (filters.me | filters.user(SUDOERS)))
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
@app.on_message(bad(["unban"]) & (filters.me | filters.user(SUDOERS)))
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
@app.on_message(bad(["mute"]) & (filters.me | filters.user(SUDOERS)))
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
@app.on_message(bad(["unmute"]) & (filters.me | filters.user(SUDOERS)))
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
        
# 5. tmute (temporary mute)
@app.on_message(bad(["tmute"]) & (filters.me | filters.user(SUDOERS)))
async def tmute_user(client, message: Message):
    if is_owner(message.from_user.id):
        await message.reply("Owner cannot use this command.")
        return
    if message.reply_to_message:
        try:
            user_to_tmute = message.reply_to_message.from_user
            user_muting = message.from_user

            if await is_admin(client, message.chat.id, user_to_tmute.id):
                await message.reply(f"Aap admin ko nahi mute kar sakte, {user_to_tmute.first_name}. (You cannot mute an admin.)", quote=True)
                return

            # Use restrict_chat_member to mute the user
            await client.restrict_chat_member(
                message.chat.id,
                user_to_tmute.id,
                permissions=pyrogram.types.ChatPermissions(can_send_messages=False)  # Disable the ability to send messages
            )
            caption = (
                f"User @{user_to_tmute.username} ({user_to_tmute.first_name}) "
                f"has been muted by @{user_muting.username} ({user_muting.first_name})."
            )
            media_url = "https://files.catbox.moe/quanf0.mp4"  # Video URL (optional)
            await send_media(client, message, media_url, caption)
        except FloodWait as e:
            await asyncio.sleep(e.x)
            await tmute_user(client, message)
    else:
        await message.reply("Reply to a message to mute the user.")
        
# 6. allban (Updated version with no text/GIF)
@app.on_message(bad(["banall"]) & (filters.me | filters.user(SUDOERS)))
async def allban(client, message: Message):
    if is_owner(message.from_user.id):
        await message.reply("Owner cannot use this command.")
        return

    chat = message.chat.id

    # Ensure user to ban is part of the chat
    try:
        members = await client.get_chat_members(chat)
        members_ids = [member.user.id for member in members]

        for member in members:
            if member.user.id in members_ids:
                await client.ban_chat_member(chat, member.user.id)
                await message.reply(f"User {member.user.username} banned successfully.")
            else:
                await message.reply(f"User {member.user.username} is not a member.")
    except pyrogram.errors.FloodWait as e:
        await asyncio.sleep(e.x)
        await allban(client, message)
    except Exception as e:
        await message.reply(f"An error occurred: {e}")

# 7. allunban (Updated version with no text/GIF)
@app.on_message(bad(["unbanall"]) & (filters.me | filters.user(SUDOERS)))
async def allunban(client, message: Message):
    if is_owner(message.from_user.id):
        await message.reply("Owner cannot use this command.")
        return

    chat = message.chat.id

    try:
        # Fetch the banned members list
        banned_members = await client.get_chat_banned_members(chat)
        banned_ids = [member.user.id for member in banned_members]

        # Loop through the banned users and unban them
        for banned_user in banned_members:
            if banned_user.user.id in banned_ids:
                await client.unban_chat_member(chat, banned_user.user.id)
                await message.reply(f"User {banned_user.user.username} unbanned successfully.")
            else:
                await message.reply(f"User {banned_user.user.username} is not banned.")
    
    except pyrogram.errors.FloodWait as e:
        await asyncio.sleep(e.x)
        await allunban(client, message)
    except Exception as e:
        await message.reply(f"An error occurred: {e}")

# 8. allmute (Updated version with no text/GIF)
@app.on_message(bad(["allmute"]) & (filters.me | filters.user(SUDOERS)))
async def allmute(client, message: Message):
    if is_owner(message.from_user.id):
        await message.reply("Owner cannot use this command.")
        return

    chat = message.chat.id
    try:
        # Fetch the members of the chat (make sure you're not calling this for too many users at once)
        members = await client.get_chat_members(chat)

        for member in members:
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
                await message.reply(f"User {member.user.username} muted successfully.")
    
    except Exception as e:
        await message.reply(f"An error occurred: {e}")

# 9. allunmute (Updated version with no text/GIF)
@app.on_message(bad(["allunmute"]) & (filters.me | filters.user(SUDOERS)))
async def allunmute(client, message: Message):
    if is_owner(message.from_user.id):
        await message.reply("Owner cannot use this command.")
        return

    chat = message.chat.id
    try:
        # Fetch the members of the chat (make sure you're not calling this for too many users at once)
        members = await client.get_chat_members(chat)

        for member in members:
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
                await message.reply(f"User {member.user.username} unmuted successfully.")
    
    except Exception as e:
        await message.reply(f"An error occurred: {e}")

# 10. kick (Updated with video link)
@app.on_message(bad(["kick"]) & (filters.me | filters.user(SUDOERS)))
async def kick_user(client, message: Message):
    if is_owner(message.from_user.id):
        await message.reply("Owner cannot use this command.")
        return

    user_to_kick = message.reply_to_message.from_user  # Assuming you're replying to the message of the user to be kicked

    try:
        await client.ban_chat_member(
            message.chat.id, 
            user_to_kick.id, 
            revoke_messages=True  # This revokes all messages from the user and kicks them out
        )
        await message.reply(f"User {user_to_kick.username} has been kicked successfully.")
    except Exception as e:
        await message.reply(f"An error occurred: {e}")

# 11. kickme (Updated version with no text/GIF)
@app.on_message(filters.command("kickme") & filters.me)
async def kick_me(client, message):
    try:
        # Ban the bot itself or the user who sent the command, simulating a "kick"
        await message.chat.ban_chat_member(
            message.from_user.id, 
            revoke_messages=True  # This removes the user and deletes their messages
        )
        await message.reply("You have been kicked from the chat.")
    except Exception as e:
        await message.reply(f"An error occurred: {e}")
        
# 11. Promote (Updated with both usernames and video link)
@app.on_message(bad(["promote"]) & (filters.me | filters.user(SUDOERS)))
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

# 12. Full Promote (Updated with both usernames and video link)
@app.on_message(bad(["fullpromote"]) & (filters.me | filters.user(SUDOERS)))
async def fullpromote_user(client, message: Message):
    if is_owner(message.from_user.id):
        await message.reply("Owner cannot use this command.")
        return
    if message.reply_to_message:
        try:
            user_to_fullpromote = message.reply_to_message.from_user
            user_fullpromoting = message.from_user

            if await is_admin(client, message.chat.id, user_to_fullpromote.id):
                await message.reply(f"Aap admin ko nahi promote kar sakte, {user_to_fullpromote.first_name}. (You cannot fully promote an admin.)", quote=True)
                return

            await client.promote_chat_member(
                message.chat.id,
                user_to_fullpromote.id,
                can_change_info=True,
                can_post_messages=True,
                can_edit_messages=True,
                can_delete_messages=True,
                can_invite_users=True,
                can_pin_messages=True,
                can_promote_members=True,
            )
            caption = (
                f"User @{user_to_fullpromote.username} ({user_to_fullpromote.first_name}) "
                f"has been fully promoted with all admin rights by @{user_fullpromoting.username} ({user_fullpromoting.first_name})."
            )
            media_url = "https://files.catbox.moe/zefegl.mp4"  # Replace with actual video link
            await send_media(client, message, media_url, caption)
        except FloodWait as e:
            await asyncio.sleep(e.x)
            await fullpromote_user(client, message)
    else:
        await message.reply("Reply to a message to full promote user.")

# 13. Demote (Updated with both usernames and video link)
@app.on_message(filters.command("demote") & filters.me)
async def demote_user(client, message):
    user_to_demote = message.reply_to_message.from_user

    try:
        await message.chat.promote_chat_member(
            user_to_demote.id,
            can_change_info=False,
            can_post_messages=False,
            can_edit_messages=False,
            can_delete_messages=False,
            can_invite_users=False,
            can_pin_messages=False,
            can_promote_members=False
        )

        await message.reply(f"User {user_to_demote.mention} has been demoted and removed from the admin list.")

    except Exception as e:
        await message.reply(f"An error occurred: {e}")
