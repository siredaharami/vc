from pyrogram import Client, filters
from pyrogram.errors import FloodWait
from pyrogram.enums import ChatMembersFilter
from BADUC.plugins.bot.clone3 import get_bot_owner  # Import the function to check bot owner
import asyncio

SPAM_CHATS = []

async def is_admin(chat_id, user_id):
    admin_ids = [
        admin.user.id
        async for admin in Client.get_chat_members(
            chat_id, filter=ChatMembersFilter.ADMINISTRATORS
        )
    ]
    if user_id in admin_ids:
        return True
    return False


async def is_authorized(client, message):
    bot_info = await client.get_me()
    bot_id = bot_info.id
    user_id = message.from_user.id
    owner_id = await get_bot_owner(bot_id)
    if owner_id != user_id:
        await message.reply_text("❌ You're not authorized to use this bot.")
        return False
    return True


@Client.on_message(filters.command(["utag"], prefixes=["/", "@"]))
async def tag_all_users(client, message):
    if not await is_authorized(client, message):
        return  # Exit if the user is not authorized

    admin = await is_admin(message.chat.id, message.from_user.id)
    if not admin:
        return

    if message.chat.id in SPAM_CHATS:
        return await message.reply_text(
            "ᴛᴀɢɢɪɴɢ ᴘʀᴏᴄᴇss ɪs ᴀʟʀᴇᴀᴅʏ ʀᴜɴɴɪɴɢ ɪғ ʏᴏᴜ ᴡᴀɴᴛ ᴛᴏ sᴛᴏᴘ sᴏ ᴜsᴇ /cancel"
        )
    replied = message.reply_to_message
    if len(message.command) < 2 and not replied:
        await message.reply_text(
            "** ɢɪᴠᴇ sᴏᴍᴇ ᴛᴇxᴛ ᴛᴏ ᴛᴀɢ ᴀʟʟ, ʟɪᴋᴇ »** `@all Hi Friends`"
        )
        return

    try:
        SPAM_CHATS.append(message.chat.id)
        usernum = 0
        usertxt = ""
        async for m in client.get_chat_members(message.chat.id):
            if message.chat.id not in SPAM_CHATS:
                break
            if m.user.is_deleted or m.user.is_bot:
                continue
            usernum += 1
            usertxt += f"[{m.user.first_name}](tg://user?id={m.user.id})  "
            if usernum == 7:
                await replied.reply_text(
                    usertxt,
                    disable_web_page_preview=True,
                )
                await asyncio.sleep(1)
                usernum = 0
                usertxt = ""
        if usernum != 0:
            await replied.reply_text(
                usertxt,
                disable_web_page_preview=True,
            )
    except FloodWait as e:
        await asyncio.sleep(e.value)
    finally:
        try:
            SPAM_CHATS.remove(message.chat.id)
        except Exception:
            pass


@Client.on_message(filters.command(["admin", "admins", "report"], prefixes=["/", "@"]) & filters.group)
async def admintag_with_reporting(client, message):
    if not await is_authorized(client, message):
        return  # Exit if the user is not authorized

    chat_id = message.chat.id
    from_user_id = message.from_user.id
    admins = [
        admin.user.id
        async for admin in client.get_chat_members(
            chat_id, filter=ChatMembersFilter.ADMINISTRATORS
        )
    ]

    if from_user_id in admins:
        return await tag_all_users(client, message)

    if len(message.text.split()) <= 1 and not message.reply_to_message:
        return await message.reply_text("Reply to a message to report that user.")

    reply = message.reply_to_message or message
    reply_user_id = reply.from_user.id if reply.from_user else reply.sender_chat.id
    if reply_user_id == Client.id:
        return await message.reply_text("Why would I report myself?")
    if reply_user_id in admins:
        return await message.reply_text("You are trying to report an admin.")

    user_mention = reply.from_user.mention if reply.from_user else "the user"
    text = f"Reported {user_mention} to admins!."

    for admin in admins:
        text += f"[\u2063](tg://user?id={admin})"

    await reply.reply_text(text)
