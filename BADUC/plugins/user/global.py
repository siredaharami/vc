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

@app.on_message(bad(["gban"]) & (filters.me | filters.user(SUDOERS)))
async def gban_user(app: Client, message: Message):
    user_id, reason = await extract_user_and_reason(message, sender_chat=True)
    if message.from_user.id != app.me.id:
        ex = await message.reply_text("`Gbanning...`")
    else:
        ex = await message.edit("`Gbanning....`")
    if not user_id:
        return await ex.edit("I can't find that user.")
    if user_id == app.me.id:
        return await ex.edit("**Okay Done... 🐽**")
    if user_id in DEVS:
        return await ex.edit("**Baap ko Mat sikha 🗿**")
    if user_id:
        try:
            user = await app.get_users(user_id)
        except Exception:
            return await ex.edit("`Please specify a valid user!`")

    if (await Zaid.gban_info(user.id)):
        return await ex.edit(
            f"[user](tg://user?id={user.id}) **it's already on the gbanned list**"
        )
    f_chats = await get_ub_chats(app)
    if not f_chats:
        return await ex.edit("**You don't have a GC that you admin 🥺**")
    er = 0
    done = 0
    for gokid in f_chats:
        try:
            await app.ban_chat_member(chat_id=gokid, user_id=int(user.id))
            done += 1
        except BaseException:
            er += 1
    await Zaid.gban_user(user.id)
    ok.append(user.id)
    msg = (
        r"**\\#GBanned_User//**"
        f"\n\n**First Name:** [{user.first_name}](tg://user?id={user.id})"
        f"\n**User ID:** `{user.id}`"
    )
    if reason:
        msg += f"\n**Reason:** `{reason}`"
    msg += f"\n**Affected To:** `{done}` **Chats**"
    await ex.edit(msg)


@app.on_message(bad(["ungban"]) & (filters.me | filters.user(SUDOERS)))
async def ungban_user(app: Client, message: Message):
    user_id, reason = await extract_user_and_reason(message, sender_chat=True)
    if message.from_user.id != app.me.id:
        ex = await message.reply("`UnGbanning...`")
    else:
        ex = await message.edit("`UnGbanning....`")
    if not user_id:
        return await ex.edit("I can't find that user.")
    if user_id:
        try:
            user = await app.get_users(user_id)
        except Exception:
            return await ex.edit("`Please specify a valid user!`")

    try:
        if not (await Zaid.gban_info(user.id)):
            return await ex.edit("`User already ungban`")
        ung_chats = await get_ub_chats(app)
        ok.remove(user.id)
        if not ung_chats:
            return await ex.edit("**You don't have a Group that you admin 🥺**")
        er = 0
        done = 0
        for good_boi in ung_chats:
            try:
                await app.unban_chat_member(chat_id=good_boi, user_id=user.id)
                done += 1
            except BaseException:
                er += 1
        await Zaid.ungban_user(user.id)
        msg = (
            r"**\\#UnGbanned_User//**"
            f"\n\n**First Name:** [{user.first_name}](tg://user?id={user.id})"
            f"\n**User ID:** `{user.id}`"
        )
        if reason:
            msg += f"\n**Reason:** `{reason}`"
        msg += f"\n**Affected To:** `{done}` **Chats**"
        await ex.edit(msg)
    except Exception as e:
        await ex.edit(f"**ERROR:** `{e}`")
        return


@app.on_message(bad(["listgban"]) & (filters.me | filters.user(SUDOERS)))
async def gbanlist(app: Client, message: Message):
    users = (await Zaid.gban_list())
    ex = await message.edit_text("`Processing...`")
    if not users:
        return await ex.edit("No Users have been Banned yet")
    gban_list = "**GBanned Users:**\n"
    count = 0
    for i in users:
        count += 1
        gban_list += f"**{count} -** `{i.sender}`\n"
    return await ex.edit(gban_list)


@app.on_message(bad(["gmute"]) & (filters.me | filters.user(SUDOERS)))
async def gmute_user(app: Client, message: Message):
    args = await extract_user(message)
    reply = message.reply_to_message
    ex = None  # Placeholder for the response message

    # Use send_message or reply if edit is not allowed
    if message.from_user.id == app.me.id:
        ex = await message.reply("`Processing...`")
    else:
        ex = await message.reply("`Processing...`")

    if args:
        try:
            user = await app.get_users(args)
        except Exception:
            await ex.edit(f"`Please specify a valid user!`")
            return
    elif reply:
        user_id = reply.from_user.id
        user = await app.get_users(user_id)
    else:
        await ex.edit(f"`Please specify a valid user!`")
        return

    if user.id == app.me.id:
        return await ex.edit("**Okay Sure.. 🐽**")
    if user.id in DEVS:
        return await ex.edit("**Baap Ko mat sikha 🗿**")

    try:
        replied_user = reply.from_user
        if replied_user.is_self:
            return await ex.edit("`Calm down anybob, you can't gmute yourself.`")
    except BaseException:
        pass

    try:
        if await Gmute.is_gmuted(user.id):
            return await ex.edit("`User already gmuted`")

        await Gmute.gmute(user.id)
        ok.append(user.id)
        await ex.edit(f"[{user.first_name}](tg://user?id={user.id}) globally gmuted!")
        
        try:
            # Apply restrictions to common chats
            common_chats = await app.get_common_chats(user.id)
            for i in common_chats:
                await i.restrict_member(user.id, ChatPermissions())
        except BaseException:
            pass

    except Exception as e:
        await ex.edit(f"**ERROR:** `{e}`")
        return


@app.on_message(bad(["ungmute"]) & (filters.me | filters.user(SUDOERS)))
async def ungmute_user(app: Client, message: Message):
    args = await extract_user(message)
    reply = message.reply_to_message
    ex = await message.edit_text("`Processing...`")
    if args:
        try:
            user = await app.get_users(args)
        except Exception:
            await ex.edit(f"`Please specify a valid user!`")
            return
    elif reply:
        user_id = reply.from_user.id
        user = await app.get_users(user_id)
    else:
        await ex.edit(f"`Please specify a valid user!`")
        return

    try:
        replied_user = reply.from_user
        if replied_user.is_self:
            return await ex.edit("`Calm down anybob, you can't ungmute yourself.`")
    except BaseException:
        pass

    try:
        if not (await Gmute.is_gmuted(user.id)):
            return await ex.edit("`User already ungmuted`")
        await Gmute.ungmute(user.id)
        ok.remove(user.id)
        try:
            common_chats = await app.get_common_chats(user.id)
            for i in common_chats:
                await i.unban_member(user.id)
        except BaseException:
            pass
        await ex.edit(
            f"[{user.first_name}](tg://user?id={user.id}) globally ungmuted!"
        )
    except Exception as e:
        await ex.edit(f"**ERROR:** `{e}`")
        return


@app.on_message(bad(["listgmute"]) & (filters.me | filters.user(SUDOERS)))
async def gmutelist(app: Client, message: Message):
    users = (await Gmute.gmute_list())
    ex = await message.edit_text("`Processing...`")
    if not users:
        return await ex.edit("There are no Muted Users yet")
    gmute_list = "**GMuted Users:**\n"
    count = 0
    for i in users:
        count += 1
        gmute_list += f"**{count} -** `{i.sender}`\n"
    return await ex.edit(gmute_list)

if ok:
 @app.on_message(filters.incoming & filters.group)
 async def globals_check(app: Client, message: Message):
    if not message:
        return
    if not message.from_user:
        return
    user_id = message.from_user.id
    chat_id = message.chat.id
    if not user_id:
        return
    if (await Zaid.gban_info(user_id)):
        try:
            await app.ban_chat_member(chat_id, user_id)
        except BaseException:
            pass

    if (await Gmute.is_gmuted(user_id)):
        try:
            await message.delete()
        except errors.RPCError:
            pass
        try:
            await app.restrict_chat_member(chat_id, user_id, ChatPermissions())
        except BaseException:
            pass

    message.continue_propagation()
