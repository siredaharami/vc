from pyrogram import Client, filters
from pyrogram.types import Message

from BADUC import SUDOERS
from BADUC.core.clients import app
from BADUC.core.command import *

@app.on_message(bad(["crate"]) & (filters.me | filters.user(SUDOERS)))
async def create(app: Client, message: Message):
    if len(message.command) < 3:
        return await message.edit_text(
            message, f"**Type .help create if you need help**"
        )
    group_type = message.command[1]
    split = message.command[2:]
    group_name = " ".join(split)
    xd = await message.edit_text("`Processing...`")
    desc = "Welcome To My " + ("Group" if group_type == "gc" else "Channel")
    if group_type == "gc":  # for supergroup
        _id = await app.create_supergroup(group_name, desc)
        link = await app.get_chat(_id["id"])
        await xd.edit(
            f"**Successfully Created Telegram Group: [{group_name}]({link['invite_link']})**",
            disable_web_page_preview=True,
        )
    elif group_type == "ch":  # for channel
        _id = await app.create_channel(group_name, desc)
        link = await app.get_chat(_id["id"])
        await xd.edit(
            f"**Successfully Created Telegram Channel: [{group_name}]({link['invite_link']})**",
            disable_web_page_preview=True,
        )

