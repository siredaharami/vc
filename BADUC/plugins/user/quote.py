import base64
import os
import time

import requests
from pyrogram import Client, filters
from pyrogram.types import Message

from BADUC import SUDOERS
from BADUC.core.clients import app
from BADUC.core.command import *


def generate_quote(messages: list[dict]) -> tuple[bool, str]:
    json = {
        "type": "quote",
        "format": "webp",
        "backgroundColor": "#260746/#6100c2",
        "width": 512,
        "height": 768,
        "scale": 2,
        "messages": messages,
    }

    try:
        response = requests.post("https://bot.lyo.su/quote/generate", json=json).json()
        image = base64.b64decode(str(response["result"]["image"]).encode("utf-8"))

        file_name = f"Quote_{int(time.time())}.webp"
        with open(file_name, "wb") as f:
            f.write(image)

        return True, file_name
    except Exception as e:
        return False, str(e)


def get_entities(message: Message) -> list[dict]:
    entities = []

    if message.entities:
        for entity in message.entities:
            entities.append(
                {
                    "type": entity.type.name.lower(),
                    "offset": entity.offset,
                    "length": entity.length,
                }
            )

    return entities

@app.on_message(bad(["q", "ss"]) & (filters.me | filters.user(SUDOERS)))
async def quotely(client: Client, message: Message):
    if not message.reply_to_message:
        return await message.delete()  # Change to delete the message object

    if message.reply_to_message.media:
        if message.reply_to_message.caption:
            message.reply_to_message.text = message.reply_to_message.caption
        else:
            return await message.delete()  # Change to delete the message object

    cmd = None
    if len(message.command) > 1:
        cmd = message.command[1].lower()

    # Rename the local variable to avoid conflict with the imported 'app'
    editing_message = await app.edit(message, "__Generating quote...__")

    msg_data = []
    if cmd and cmd == "r":
        await editing_message.edit("__Generating quote with reply...__")
        reply_msg_id = message.reply_to_message.reply_to_message_id
        if reply_msg_id:
            reply_msg = await client.get_messages(message.chat.id, reply_msg_id)
            if reply_msg and reply_msg.text:
                replied_name = reply_msg.from_user.first_name
                if reply_msg.from_user.last_name:
                    replied_name += f" {reply_msg.from_user.last_name}"

                reply_message = {
                    "chatId": reply_msg.from_user.id,
                    "entities": get_entities(reply_msg),
                    "name": replied_name,
                    "text": reply_msg.text,
                }
            else:
                reply_message = {}
        else:
            reply_message = {}
    else:
        reply_message = {}

    name = message.reply_to_message.from_user.first_name
    if message.reply_to_message.from_user.last_name:
        name += f" {message.reply_to_message.from_user.last_name}"

    emoji_status = None
    if message.reply_to_message.from_user.emoji_status:
        emoji_status = str(message.reply_to_message.from_user.emoji_status.custom_emoji_id)

    msg_data.append(
        {
            "entities": get_entities(message.reply_to_message),
            "avatar": True,
            "from": {
                "id": message.reply_to_message.from_user.id,
                "name": name,
                "emoji_status": emoji_status,
            },
            "text": message.reply_to_message.text,
            "replyMessage": reply_message,
        }
    )

    status, path = generate_quote(msg_data)
    if not status:
        return await editing_message.error(message, f"`{path}`")

    await message.reply_sticker(path)
    await editing_message.delete()
    os.remove(path)

