from BADUC import SUDOERS
from BADUC.core.clients import app
from BADUC.core.command import *
from pyrogram.errors import RPCError
from typing import List
from pyrogram import Client, errors, filters
from pyrogram.types import ChatPermissions, Message
from BADUC.database.gchat import get_ub_chats
from BADUC.database.misc import extract_user, extract_user_and_reason
from BADUC.database import gbandb as Zaid
from BADUC.database import gmutedb as Gmute

ok = []

DEVS = [7009601543]

# GBAN Function
@app.on_message(bad(["gban"]) & (filters.me | filters.user(SUDOERS)))
async def gban_user(app: Client, message: Message):
    user_id, reason = await extract_user_and_reason(message, sender_chat=True)
    ex = await message.reply_text("`Processing...`")

    if not user_id:
        return await ex.edit("`I can't find that user.`")
    if user_id == app.me.id:
        return await ex.edit("**You can't gban yourself! 🐽**")
    if user_id in DEVS:
        return await ex.edit("**You can't gban a developer! 🗿**")

    try:
        user = await app.get_users(user_id)
    except Exception:
        return await ex.edit("`Please specify a valid user!`")

    if await Zaid.gban_info(user.id):
        return await ex.edit(f"[{user.first_name}](tg://user?id={user.id}) is already gbanned.")

    f_chats = await get_ub_chats(app)
    if not f_chats:
        return await ex.edit("`No groups found where you're an admin.`")

    er = 0
    done = 0
    for chat in f_chats:
        try:
            await app.ban_chat_member(chat, user.id)
            done += 1
        except BaseException:
            er += 1

    await Zaid.gban_user(user.id)
    ok.append(user.id)

    msg = (
        r"**\\#GBanned_User//**"
        f"\n**Name:** [{user.first_name}](tg://user?id={user.id})"
        f"\n**User ID:** `{user.id}`"
        f"\n**Reason:** `{reason}`" if reason else ""
        f"\n**Affected Chats:** `{done}`"
    )
    await ex.edit(msg)


# UNGBAN Function
@app.on_message(bad(["ungban"]) & (filters.me | filters.user(SUDOERS)))
async def ungban_user(app: Client, message: Message):
    user_id, reason = await extract_user_and_reason(message, sender_chat=True)
    ex = await message.reply_text("`Processing...`")

    if not user_id:
        return await ex.edit("`I can't find that user.`")

    try:
        user = await app.get_users(user_id)
    except Exception:
        return await ex.edit("`Please specify a valid user!`")

    if not await Zaid.gban_info(user.id):
        return await ex.edit(f"`[{user.first_name}](tg://user?id={user.id}) is not gbanned.`")

    f_chats = await get_ub_chats(app)
    if not f_chats:
        return await ex.edit("`No groups found where you're an admin.`")

    er = 0
    done = 0
    for chat in f_chats:
        try:
            await app.unban_chat_member(chat, user.id)
            done += 1
        except BaseException:
            er += 1

    await Zaid.ungban_user(user.id)
    ok.remove(user.id)

    msg = (
        r"**\\#UnGbanned_User//**"
        f"\n**Name:** [{user.first_name}](tg://user?id={user.id})"
        f"\n**User ID:** `{user.id}`"
        f"\n**Reason:** `{reason}`" if reason else ""
        f"\n**Affected Chats:** `{done}`"
    )
    await ex.edit(msg)


# GBAN List Function
@app.on_message(bad(["listgban"]) & (filters.me | filters.user(SUDOERS)))
async def gbanlist(app: Client, message: Message):
    users = await Zaid.gban_list()
    ex = await message.reply_text("`Processing...`")

    if not users:
        return await ex.edit("`No users have been gbanned yet.`")

    gban_list = "**GBanned Users:**\n"
    for count, user in enumerate(users, start=1):
        gban_list += f"**{count}.** `{user.sender}`\n"

    await ex.edit(gban_list)


# GMUTE Function
@app.on_message(bad(["gmute"]) & (filters.me | filters.user(SUDOERS)))
async def gmute_user(app: Client, message: Message):
    user_id, reason = await extract_user_and_reason(message)
    ex = await message.reply_text("`Processing...`")

    # Check if user exists and is valid
    if not user_id:
        return await ex.edit("`I can't find that user.`")
    if user_id == app.me.id:
        return await ex.edit("`You can't gmute yourself!`")
    if user_id in DEVS:
        return await ex.edit("`You can't gmute a developer!`")

    try:
        user = await app.get_users(user_id)
    except Exception:
        return await ex.edit("`Please specify a valid user!`")

    # Check if already globally muted
    if await Gmute.is_gmuted(user.id):
        return await ex.edit(f"`[{user.first_name}](tg://user?id={user.id}) is already gmuted.`")

    # Add to GMUTE database
    await Gmute.gmute(user.id)
    ok.append(user.id)

    # Restrict user in common chats
    common_chats = await app.get_common_chats(user.id)
    restricted = 0
    errors = 0

    for chat in common_chats:
        try:
            await app.restrict_chat_member(chat.id, user.id, ChatPermissions())
            restricted += 1
        except Exception:
            errors += 1

    # Prepare success message
    msg = (
        f"**\\#GMuted_User//**\n\n"
        f"**Name:** [{user.first_name}](tg://user?id={user.id})\n"
        f"**User ID:** `{user.id}`\n"
        f"**Reason:** `{reason}`\n" if reason else ""
        f"**Restricted in:** `{restricted}` chats.\n"
        f"**Errors in:** `{errors}` chats."
    )
    await ex.edit(msg)

@app.on_message(filters.group & filters.incoming)
async def enforce_gmute(app: Client, message: Message):
    if not message.from_user:
        return

    user_id = message.from_user.id
    chat_id = message.chat.id

    # Check if the user is globally muted
    if await Gmute.is_gmuted(user_id):
        try:
            # Delete the message
            await message.delete()
        except errors.RPCError:
            pass

        try:
            # Ensure the user is restricted
            await app.restrict_chat_member(chat_id, user_id, ChatPermissions())
        except BaseException:
            pass

# UNGMUTE Function
@app.on_message(bad(["ungmute"]) & (filters.me | filters.user(SUDOERS)))
async def ungmute_user(app: Client, message: Message):
    ex = await message.reply_text("`Processing...`")

    # Extract user from command or reply
    args = await extract_user(message)  # Ensure this function works as intended.
    reply = message.reply_to_message

    if args:
        try:
            user = await app.get_users(args)
        except Exception as e:
            return await ex.edit(f"Invalid user specified! Error: {e}")
    elif reply:
        user = reply.from_user
    else:
        return await ex.edit("Please specify a user to unmute!")

    # Check if the user is globally muted
    is_gmuted = await Gmute.is_gmuted(user.id)
    if not is_gmuted:
        return await ex.edit(f"[{user.first_name}](tg://user?id={user.id}) is not globally muted.")

    # Remove user from global mute list
    await Gmute.ungmute(user.id)

    # Unban the user from common chats
    try:
        common_chats = await app.get_common_chats(user.id)
        for chat in common_chats:
            try:
                await app.unban_chat_member(chat.id, user.id)
            except Exception as e:
                print(f"Failed to unban in chat {chat.id}: {e}")
    except Exception as e:
        print(f"Error fetching common chats: {e}")

    # Confirm unmute
    await ex.edit(f"[{user.first_name}](tg://user?id={user.id}) has been globally unmuted!")


# GMUTE List Function
@app.on_message(bad(["listgmute"]) & (filters.me | filters.user(SUDOERS)))
async def list_gmuted_users(app: Client, message: Message):
    """
    Lists all globally muted users.
    """
    # Fetch the list of globally muted users
    users = await Gmute.gmute_list()
    ex = await message.edit_text("`Processing...`")
    
    if not users:
        await ex.edit("There are no globally muted users yet.")
        return
    
    # Prepare the list of muted users
    gmute_list = "**GMuted Users:**\n"
    for count, user in enumerate(users, start=1):
        gmute_list += f"**{count} -** `{user.sender}`\n"
    
    await ex.edit(gmute_list)

# Function to check global restrictions
@app.on_message(filters.incoming & filters.group)
async def global_restrictions_check(app: Client, message: Message):
    """
    Checks if the user is globally muted or banned, and applies restrictions.
    """
    if not message or not message.from_user:
        return

    user_id = message.from_user.id
    chat_id = message.chat.id

    # Handle globally banned users
    if await Zaid.gban_info(user_id):
        try:
            await app.ban_chat_member(chat_id, user_id)
        except Exception as e:
            print(f"Failed to ban user {user_id} in chat {chat_id}: {e}")

    # Handle globally muted users
    if await Gmute.is_gmuted(user_id):
        try:
            await message.delete()
        except RPCError as e:
            print(f"Failed to delete message from muted user {user_id}: {e}")
        
        try:
            await app.restrict_chat_member(chat_id, user_id, ChatPermissions())
        except Exception as e:
            print(f"Failed to restrict user {user_id} in chat {chat_id}: {e}")

    message.continue_propagation()
