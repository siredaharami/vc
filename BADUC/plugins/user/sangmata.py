import asyncio

from pyrogram import *
from pyrogram import filters
from pyrogram.errors import YouBlockedUser
from pyrogram.types import *
from BADUC import SUDOERS
from BADUC.core.clients import app
from BADUC.core.command import *
from BADUC.database.misc import *

@app.on_message(bad(["sg"]) & (filters.me | filters.user(SUDOERS)))
async def sg(client: Client, message: Message):
    args = await extract_user(message)
    lol = await message.edit_text("`ᴘʀᴏᴄᴇꜱꜱɪɴɢ...`")
    if args:
        try:
            user = await client.get_users(args)
        except Exception:
            return await lol.edit(f"`ᴘʟᴇᴀꜱᴇ ꜱᴘᴇᴄɪꜰʏ ᴀ ᴠᴀʟɪᴅ ᴜꜱᴇʀ!`")
    bot = "SangMataInfo_bot"
    try:
        await client.send_message(bot, f"/search_id {user.id}")
    except YouBlockedUser:
        await client.unblock_user(bot)
        await client.send_message(bot, f"/search_id {user.id}")
    await asyncio.sleep(1)

    async for stalk in client.search_messages(bot, query="Name", limit=1):
        if not stalk:
            await message.edit_text("ᴛʜɪꜱ ᴘᴇʀꜱᴏɴ ʜᴀꜱ ɴᴇᴠᴇʀ ᴄʜᴀɴɢᴇᴅ ʜɪꜱ ɴᴀᴍᴇ")
            return
        elif stalk:
            await message.edit(stalk.text)
            await stalk.delete()

    async for stalk in client.search_messages(bot, query="Username", limit=1):
        if not stalk:
            return
        elif stalk:
            await message.reply(stalk.text)
            await stalk.delete()





__NAME__ = "Hɪsᴛᴏʀʏ"
__MENU__ = """
`.sg` - **Get All Names
and Usernames History.**

**Alternate Command:** '`whois`'
"""
