import asyncio
from pyrogram import filters, Client
from pyrogram.raw import functions, types
from pyrogram.types import Message

from BADUC import SUDOERS
from BADUC.core.clients import app
from BADUC.core.command import *

@app.on_message(bad(["ss"]) & (filters.me | filters.user(SUDOERS)))
async def screenshot(bot: Client, message: Message):
    # Properly await message deletion
    await message.delete()

    try:
        # Ensure peer is properly resolved
        peer = await bot.resolve_peer(message.chat.id)

        # Use SendScreenshotNotification with proper arguments
        await bot.invoke(
            functions.messages.SendScreenshotNotification(
                peer=peer,
                random_id=bot.rnd_id(),
                reply_to=None,  # None or a valid reply_to message ID
            )
        )
    except Exception as e:
        print(f"Error sending screenshot notification: {e}")
