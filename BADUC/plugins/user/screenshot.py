import asyncio

from pyrogram import filters, Client 
from pyrogram.raw import functions
from pyrogram.types import Message

from BADUC import SUDOERS
from BADUC.core.clients import app
from BADUC.core.command import *



@app.on_message(bad(["ss"]) & (filters.me | filters.user(SUDOERS)))
async def screenshot(bot: Client, message: Message):
    await asyncio.gather(
        message.delete(),
        bot.send(
            functions.messages.SendScreenshotNotification(
                peer=await bot.resolve_peer(message.chat.id),
                reply_to_msg_id=0,
                random_id=bot.rnd_id(),
            )
        ),
    )
  
