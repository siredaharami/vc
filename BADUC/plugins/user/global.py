from BADUC import SUDOERS
from BADUC.core.clients import app
from BADUC.core.command import *
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
    args = await extract_user(message)
    reply = message.reply_to_message
    ex = await message.reply_text("`Processing...`")

    if args:
        try:
            user = await app.get_users(args)
        except Exception:
            return await ex.edit("`Please specify a valid user!`")
    elif reply:
        user = reply.from_user
    else:
        return await ex.edit("`Please specify a valid user!`")

    if user.id == app.me.id:
        return await ex.edit("`You can't gmute yourself!`")
    if user.id in DEVS:
        return await ex.edit("`You can't gmute a developer!`")

    if await Gmute.is_gmuted(user.id):
        return await ex.edit(f"`[{user.first_name}](tg://user?id={user.id}) is already gmuted.`")

    await Gmute.gmute(user.id)
    ok.append(user.id)

    try:
        common_chats = await app.get_common_chats(user.id)
        for chat in common_chats:
            await app.restrict_chat_member(chat.id, user.id, ChatPermissions())
    except BaseException:
        pass

    await ex.edit(f"`[{user.first_name}](tg://user?id={user.id}) has been globally muted!`")


# UNGMUTE Function
@app.on_message(bad(["ungmute"]) & (filters.me | filters.user(SUDOERS)))
async def ungmute_user(app: Client, message: Message):
    args = await extract_user(message)
    reply = message.reply_to_message
    ex = await message.reply_text("`Processing...`")

    if args:
        try:
            user = await app.get_users(args)
        except Exception:
            return await ex.edit("`Please specify a valid user!`")
    elif reply:
        user = reply.from_user
    else:
        return await ex.edit("`Please specify a valid user!`")

    if not await Gmute.is_gmuted(user.id):
        return await ex.edit(f"`[{user.first_name}](tg://user?id={user.id}) is not gmuted.`")

    await Gmute.ungmute(user.id)
    ok.remove(user.id)

    try:
        common_chats = await app.get_common_chats(user.id)
        for chat in common_chats:
            await app.unban_chat_member(chat.id, user.id)
    except BaseException:
        pass

    await ex.edit(f"`[{user.first_name}](tg://user?id={user.id}) has been globally unmuted!`")


# GMUTE List Function
@app.on_message(bad(["listgmute"]) & (filters.me | filters.user(SUDOERS)))
async def gmutelist(app: Client, message: Message):
    users = await Gmute.gmute_list()
    ex = await message.reply_text("`Processing...`")

    if not users:
        return await ex.edit("`No users have been gmuted yet.`")

    gmute_list = "**GMuted Users:**\n"
    for count, user in enumerate(users, start=1):
        gmute_list += f"**{count}.** `{user.sender}`\n"

    await ex.edit(gmute_list)
