import asyncio
from pyrogram import filters, Client
from pyrogram.raw import functions
from pyrogram.types import Message

from BADUC import SUDOERS
from BADUC.core.clients import app
from BADUC.core.command import *

@app.on_message(bad(["ss"]) & (filters.me | filters.user(SUDOERS)))
async def screenshot(bot: Client, message: Message):
    # Properly await the delete coroutine
    await message.delete()

    # Add the required 'reply_to' argument
    try:
        await bot.send(
            functions.messages.SendScreenshotNotification(
                peer=await bot.resolve_peer(message.chat.id),
                random_id=bot.rnd_id(),
                reply_to=0  # Set appropriately (e.g., message ID to reply to)
            )
        )
    except Exception as e:
        print(f"Error sending screenshot notification: {e}")
