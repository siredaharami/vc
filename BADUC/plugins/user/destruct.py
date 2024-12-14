import os
from BADUC import SUDOERS
from BADUC.core.clients import app
from BADUC.core.command import *
from pyrogram import filters


@app.on_message(bad(["🙈🙈"]) & (filters.me | filters.user(SUDOERS)))
    & filters.private & filters.me)
async def self_media(client, message):
    try:
        replied = message.reply_to_message
        if not replied:
            return
        if not (replied.photo or replied.video):
            return
        location = await client.download_media(replied)
        await client.send_document("me", location)
        os.remove(location)
    except Exception as e:
        print("Error: `{e}`")
        return
