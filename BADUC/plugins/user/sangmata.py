import asyncio
from pyrogram import Client
from pyrogram import *
from pyrogram import filters
from pyrogram.errors import YouBlockedUser
from pyrogram.raw.functions.messages import DeleteHistory
from pyrogram.types import *

from BADUC.database.basic import edit_or_reply
from BADUC.database.sangmatadb import extract_user
from BADUC import SUDOERS
from BADUC.core.clients import app
from BADUC.core.command import *

@app.on_message(bad(["sg"]) & (filters.me | filters.user(SUDOERS)))
async def sg(client: Client, message: Message):
    args = await extract_user(message)
    lol = await edit_or_reply(message, "`ᴘʀᴏᴄᴇꜱꜱɪɴɢ...`")

    # Check if args is provided and valid
    if args:
        try:
            user = await client.get_users(args)
        except Exception:
            return await lol.edit(f"`ᴘʟᴇᴀꜱᴇ ꜱᴘᴇᴄɪꜰʏ ᴀ ᴠᴀʟɪᴅ ᴜꜱᴇʀ!`")
    else:
        return await lol.edit(f"`ᴘʟᴇᴀꜱᴇ ꜱᴘᴇᴄɪꜰʏ ᴀ ᴠᴀʟɪᴅ ᴜꜱᴇʀ!`")

    bot = "@SangMataInfo_bot"
    try:
        await client.send_message(bot, f"{user.id}")
    except YouBlockedUser:
        await client.unblock_user(bot)
        await client.send_message(bot, f"{user.id}")
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
    
    user_info = await client.resolve_peer(bot)
    return await client.send(DeleteHistory(peer=user_info, max_id=0, revoke=True))
