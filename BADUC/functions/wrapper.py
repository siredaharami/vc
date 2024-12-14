from pyrogram.types import *
from traceback import format_exc

from BADUC import SUDOERS
from BADUC.core.clients import app, bot

def super_user_only(mystic):
    async def wrapper(client, message):
        try:
            if message.from_user.is_self:
                return await mystic(client, message)
        except:
            if message.outgoing:
                return await mystic(client, message)
    return wrapper

def sudo_user(mystic):
    async def wrapper(client, message):
        try:
            if (message.from_user.is_self or
               message.from_user.id in SUDOERS):
                return await mystic(client, message)
        except:
            if (message.outgoing or
               message.from_user.id in SUDOERS):
                return await mystic(client, message)
    return wrapper

def cb_wrapper(func):
    async def wrapper(bot, cb):
        sudousers = SUDOERS
        if (cb.from_user.id != app.me.id and
            cb.from_user.id not in sudousers):
            return await cb.answer(
                "🥺 ʏᴏᴜ ᴀʀᴇ ɴᴏᴛ ᴀ ꜱᴜᴅᴏ ᴜꜱᴇʀ❗",
                cache_time=0,
                show_alert=True,
            )
        else:
            try:
                return await func(bot, cb)
            except Exception:
                print(format_exc())
                return await cb.answer(
                    f"🤖 ꜱᴏᴍᴇᴛʜɪɴɢ ᴡᴇɴᴛ ᴡʀᴏɴɢ, ᴘʟᴇᴀꜱᴇ ᴄʜᴇᴄᴋ ʟᴏɢꜱ❗..."
                )
    return wrapper

def inline_wrapper(func):
    from BADUC import __version__
    async def wrapper(bot, query):
        sudousers = SUDOERS
        if (query.from_user.id != app.me.id and
            query.from_user.id not in sudousers):
            try:
                button = [
                    [
                        InlineKeyboardButton(
                            "💫 ᴅᴇᴘʟᴏʏ ʏᴏᴜʀ ᴏᴡɴ ʙᴀᴅᴜꜱᴇʀʙᴏᴛ ❤️",
                            url=f"https://github.com/Badhacker98/BAD_USERBOT/fork"
                        )
                    ]
                ]
                await bot.answer_inline_query(
                    query.id,
                    cache_time=1,
                    results=[
                        InlineQueryResultPhoto(
                            photo_url="https://files.catbox.moe/83d5lc.jpg",
                            title="🥀 ʙᴀᴅᴜꜱᴇʀʙᴏᴛ ✨",
                            thumb_url="https://files.catbox.moe/83d5lc.jpg",
                            description="🌸 ᴅᴇᴘʟᴏʏ ʏᴏᴜʀ ᴏᴡɴ ʙᴀᴅᴜꜱᴇʀʙᴏᴛ 💕...",
                            caption=f"<b>🥀 ᴡᴇʟᴄᴏᴍᴇ » ᴛᴏ » ʙᴀᴅᴜᴄ 🌷\n✅ ᴜꜱᴇʀʙᴏᴛ {__version__} ✨...</b>",
                            reply_markup=InlineKeyboardMarkup(button),
                        )
                    ],
                )
            except Exception as e:
                print(format_exc())
                await bot.answer_inline_query(
                    query.id,
                    cache_time=1,
                    results=[
                        InlineQueryResultArticle(
                            title="⚜️ ᴅᴇᴘʟᴏʏ ʏᴏᴜʀ ᴏᴡɴ ʙᴀᴅᴜꜱᴇʀʙᴏᴛ ⚜️",
                            input_message_content=InputTextMessageContent(
                                f"🥀 ᴘʟᴇᴀꜱᴇ, ᴅᴇᴘʟᴏʏ ʏᴏᴜʀ ᴏᴡɴ ʙᴀᴅᴜꜱᴇʀʙᴏᴛ❗...\n\nʀᴇᴘᴏ - [ᴠɪᴇᴡ](https://github.com/Badhacker98/BAD_USERBOT/fork)"
                            ),
                        )
                    ],
                )
        else:
            try:
                return await func(bot, query)
            except Exception as e:
                print(format_exc())
    return wrapper
  
