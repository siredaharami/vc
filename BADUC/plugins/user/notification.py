from BADUC import SUDOERS
from BADUC.core.clients import app
from BADUC.core.command import *

from pyrogram import Client, enums, filters 
from pyrogram.types import Message 
from BADUC.core.config import LOG_GROUP_ID as LOG_GROUP
log = []


@app.on_message(bad(["tagalert on"]) & (filters.me | filters.user(SUDOERS)))
async def set_no_log_p_m(app: Client, message: Message):
    if LOG_GROUP != -100:
        if not message.chat.id in log:
            log.append(message.chat.id)
            await message.edit("**Tag alert Activated Successfully**")

@app.on_message(bad(["tagalert off"]) & (filters.me | filters.user(SUDOERS)))
async def set_no_log_p_m(app: Client, message: Message):
        if not message.chat.id in log:
            log.remove(message.chat.id)
            await message.edit("**Tag alert DeActivated Successfully**")

if log:
 @app.on_message(filters.group & filters.mentioned & filters.incoming)
 async def log_tagged_messages(app: Client, message: Message):
    result = f"<b>📨 #TAGS #MESSAGE</b>\n<b> • : </b>{message.from_user.mention}"
    result += f"\n<b> • Group : </b>{message.chat.title}"
    result += f"\n<b> • 👀 </b><a href = '{message.link}'>Lihat Pesan</a>"
    result += f"\n<b> • Message : </b><code>{message.text}</code>"
    await asyncio.sleep(0.5)
    await app.send_message(
        LOG_GROUP,
        result,
        parse_mode=enums.ParseMode.HTML,
        disable_web_page_preview=True,
    )

