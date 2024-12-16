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

            await client.mute_chat_member(message.chat.id, user_to_mute.id)  # Correct method for muting
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

            await client.unmute_chat_member(message.chat.id, user_to_unmute.id)  # Correct method for unmuting
            caption = (
                f"User @{user_to_unmute.username} ({user_to_unmute.first_name}) "
                f"has been unmuted by @{user_unmuting.username} ({user_unmuting.first_name})."
            )
            media_url = "https://files.catbox.moe/rudmdy.mp4"  # Video URL
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
            user_tmuting = message.from_user

            if await is_admin(client, message.chat.id, user_to_tmute.id):
                await message.reply(f"Aap admin ko nahi mute kar sakte, {user_to_tmute.first_name}. (You cannot mute an admin.)", quote=True)
                return

            await client.mute_chat_member(message.chat.id, user_to_tmute.id)  # Correct method for muting
            caption = (
                f"User @{user_to_tmute.username} ({user_to_tmute.first_name}) "
                f"has been temporarily muted by @{user_tmuting.username} ({user_tmuting.first_name})."
            )
            media_url = "https://files.catbox.moe/gccjzy.mp4"  # Video URL
            await send_media(client, message, media_url, caption)
            await asyncio.sleep(600)  # 10 minutes mute

            await client.unmute_chat_member(message.chat.id, user_to_tmute.id)  # Correct method for unmuting
            caption = (
                f"User @{user_to_tmute.username} ({user_to_tmute.first_name})'s mute has been lifted by "
                f"@{user_tmuting.username} ({user_tmuting.first_name})."
            )
            await send_media(client, message, media_url, caption)
        except FloodWait as e:
            await asyncio.sleep(e.x)
            await tmute_user(client, message)
    else:
        await message.reply("Reply to a message to temporarily mute user.")
        
# 6. allban (Updated version with no text/GIF)
@app.on_message(bad(["banall"]) & (filters.me | filters.user(SUDOERS)))
async def allban(client, message: Message):
    if is_owner(message.from_user.id):
        await message.reply("Owner cannot use this command.")
        return
    chat = message.chat.id
    try:
        async for member in client.get_chat_members(chat):
            if member.status in ["administrator", "creator"]:
                continue
            await client.ban_chat_member(chat, member.user.id)  # Correct method for banning
        # No text or GIF, just execute the ban silently
    except FloodWait as e:
        await asyncio.sleep(e.x)
        await allban(client, message)

# 7. allunban (Updated version with no text/GIF)
@app.on_message(bad(["unbanall"]) & (filters.me | filters.user(SUDOERS)))
async def allunban(client, message: Message):
    if is_owner(message.from_user.id):
        await message.reply("Owner cannot use this command.")
        return
    chat = message.chat.id
    try:
        async for member in client.get_chat_members(chat):
            if member.status in ["administrator", "creator"]:
                continue
            await client.unban_chat_member(chat, member.user.id)  # Correct method for unbanning
        # No text or GIF, just execute the unban silently
    except FloodWait as e:
        await asyncio.sleep(e.x)
        await allunban(client, message)

# 8. allmute (Updated version with no text/GIF)
@app.on_message(bad(["allmute"]) & (filters.me | filters.user(SUDOERS)))
async def allmute(client, message: Message):
    if is_owner(message.from_user.id):
        await message.reply("Owner cannot use this command.")
        return
    chat = message.chat.id
    try:
        async for member in client.get_chat_members(chat):
            if member.status in ["administrator", "creator"]:
                continue
            await client.mute_chat_member(chat, member.user.id)  # Correct method for muting
        # No text or GIF, just execute the mute silently
    except FloodWait as e:
        await asyncio.sleep(e.x)
        await allmute(client, message)

# 9. allunmute (Updated version with no text/GIF)
@app.on_message(bad(["allunmute"]) & (filters.me | filters.user(SUDOERS)))
async def allunmute(client, message: Message):
    if is_owner(message.from_user.id):
        await message.reply("Owner cannot use this command.")
        return
    chat = message.chat.id
    try:
        async for member in client.get_chat_members(chat):
            if member.status in ["administrator", "creator"]:
                continue
            await client.unmute_chat_member(chat, member.user.id)  # Correct method for unmuting
        # No text or GIF, just execute the unmute silently
    except FloodWait as e:
        await asyncio.sleep(e.x)
        await allunmute(client, message)

# 10. kick (Updated with video link)
@app.on_message(bad(["kick"]) & (filters.me | filters.user(SUDOERS)))
async def kick_user(client, message: Message):
    if is_owner(message.from_user.id):
        await message.reply("Owner cannot use this command.")
        return
    if message.reply_to_message:
        try:
            user_to_kick = message.reply_to_message.from_user
            user_kicking = message.from_user

            # Check if the user being kicked is an admin
            if await is_admin(client, message.chat.id, user_to_kick.id):
                await message.reply(f"Aap admin ko nahi kick kar sakte, {user_to_kick.first_name}. (You cannot kick an admin.)", quote=True)
                return

            # Kick the user
            await client.kick_chat_member(message.chat.id, user_to_kick.id)  # Correct method for kicking

            # Prepare message with both usernames
            caption = (
                f"User @{user_to_kick.username} ({user_to_kick.first_name}) "
                f"has been kicked from the group by @{user_kicking.username} ({user_kicking.first_name})."
            )
            media_url = "https://files.catbox.moe/btsqh4.mp4"  # Video URL
            await send_media(client, message, media_url, caption)
        except FloodWait as e:
            await asyncio.sleep(e.x)
            await kick_user(client, message)
    else:
        await message.reply("Reply to a message to kick user.")

# 11. kickme (Updated version with no text/GIF)
@app.on_message(bad(["kickme"]) & (filters.me | filters.user(SUDOERS)))
async def kick_me(client, message: Message):
    if is_owner(message.from_user.id):
        await message.reply("Owner cannot use this command.")
        return
    try:
        if len(message.command) > 1:
            link = message.command[1]  # The second word is expected to be the URL
            await message.reply(f"Here is the link: {@PBX_CHAT}")
        else:
            await message.reply("No link provided. You will be kicked.")
        
        await message.chat.kick_member(message.from_user.id)
    except FloodWait as e:
        await asyncio.sleep(e.x)
        await kick_me(client, message)
        
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
@app.on_message(bad(["demote"]) & (filters.me | filters.user(SUDOERS)))
async def demote_user(client, message: Message):
    if is_owner(message.from_user.id):
        await message.reply("Owner cannot use this command.")
        return
    if message.reply_to_message:
        try:
            user_to_demote = message.reply_to_message.from_user
            user_demoting = message.from_user

            if not await is_admin(client, message.chat.id, user_to_demote.id):
                await message.reply(f"{user_to_demote.first_name} is not an admin.", quote=True)
                return

            await client.promote_chat_member(
                message.chat.id,
                user_to_demote.id,
                can_change_info=False,
                can_post_messages=False,
                can_edit_messages=False,
                can_delete_messages=False,
                can_invite_users=False,
                can_pin_messages=False,
                can_promote_members=False,
            )
            caption = (
                f"User @{user_to_demote.username} ({user_to_demote.first_name}) "
                f"has been demoted from admin by @{user_demoting.username} ({user_demoting.first_name})."
            )
            media_url = "https://files.catbox.moe/4q73uq.mp4"  # Replace with actual video link
            await send_media(client, message, media_url, caption)
        except FloodWait as e:
            await asyncio.sleep(e.x)
            await demote_user(client, message)
    else:
        await message.reply("Reply to a message to demote user.")
        
# 14. All Demote (Updated with video link)
@app.on_message(bad(["alldemote"]) & (filters.me | filters.user(SUDOERS)))
async def alldemote(client, message: Message):
    if is_owner(message.from_user.id):
        await message.reply("Owner cannot use this command.")
        return
    chat = message.chat.id
    try:
        async for member in client.get_chat_members(chat):
            if member.status not in ["administrator", "creator"]:
                continue
            await client.promote_chat_member(
                chat,
                member.user.id,
                can_change_info=False,
                can_post_messages=False,
                can_edit_messages=False,
                can_delete_messages=False,
                can_invite_users=False,
                can_pin_messages=False,
                can_promote_members=False,
            )
        caption = "All admins have been demoted from their positions."
        media_url = "https://files.catbox.moe/n63pxf.mp4"  # Replace with actual video link
        await send_media(client, message, media_url, caption)
    except FloodWait as e:
        await asyncio.sleep(e.x)
        await alldemote(client, message)
