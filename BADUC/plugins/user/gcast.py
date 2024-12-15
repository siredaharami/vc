from pyrogram import Client
from pyrogram.enums import ParseMode
from pyrogram.types import Message


from BADUC import SUDOERS
from BADUC.core.clients import app
from BADUC.core.command import *

gcast = Gcast()


@app.on_message(bad(["gcast", "broadcast"]) & (filters.me | filters.user(SUDOERS)))
async def broadcast(client: Client, message: Message):
    if len(message.command) < 2 or not message.reply_to_message:
        return await app.delete(
            message,
            f"Reply to a message with .gcast <all / groups / users> <copy>",
        )

    mode = message.command[1].lower()
    if mode not in ["all", "groups", "users"]:
        return await app.delete(
            message,
            f"Reply to a message with .gcast <all / groups / users> <copy>",
        )

    tag = True
    if len(message.command) > 2:
        is_copy = message.command[2].lower()
        tag = False if is_copy == "copy" else True

    app = await app.edit(message, "Processing...")
    msg = await gcast.start(
        message.reply_to_message, client, message.command[1].strip(), tag
    )

    if msg:
        await app.edit(
            msg[1], parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True
        )
        await app.check_and_log("gcast", msg[1], msg[0])
    else:
        await app.edit("No user or group found!")

