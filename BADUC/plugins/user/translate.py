from pyrogram import filters
from pyrogram.types import *
from gpytranslate import Translator
from BADUC import SUDOERS
from BADUC.core.clients import app
from BADUC.core.command import *

trans = Translator()

@app.on_message(bad(["tr"]) & (filters.me | filters.user(SUDOERS)))
async def translate(_, message) -> None:
    reply_msg = message.reply_to_message
    if not reply_msg:
        await message.reply_text("ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴍᴇssᴀɢᴇ ᴛᴏ ᴛʀᴀɴsʟᴀᴛᴇ ɪᴛ!")
        await message.delete()
        return
    if reply_msg.caption:
        to_translate = reply_msg.caption
    elif reply_msg.text:
        to_translate = reply_msg.text
    else:
        await message.reply_text("ɴᴏ ᴛᴇxᴛ ғᴏᴜɴᴅ ᴛᴏ ᴛʀᴀɴsʟᴀᴛᴇ!")
        await message.delete()
        return

    try:
        args = message.text.split()[1].lower()
        if "//" in args:
            source = args.split("//")[0]
            dest = args.split("//")[1]
        else:
            source = await trans.detect(to_translate)
            dest = args
    except IndexError:
        source = await trans.detect(to_translate)
        dest = "en"

    try:
        translation = await trans(to_translate, sourcelang=source, targetlang=dest)
        reply = (
            f"ᴛʀᴀɴsʟᴀᴛᴇᴅ ғʀᴏᴍ {source} ᴛᴏ {dest}:\n"
            f"{translation.text}"
        )
        await reply_msg.reply_text(reply)
    except Exception as e:
        await message.reply_text(f"Error: {e}")
    finally:
        await message.delete()

__NAME__ = "Tʀᴀɴsʟᴀᴛᴇ"
__MENU__ = """
`.tr` - **Translate some text by giving a language code or replying to a text/caption.**
"""
