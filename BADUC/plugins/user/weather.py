import asyncio
from html import escape

import aiohttp
from pyrogram import filters, Client 
from pyrogram.types import Message
from BADUC import SUDOERS
from BADUC.core.clients import app
from BADUC.core.command import *

from pyrogram import enums

@app.on_message(bad(["weather"]) & (filters.me | filters.user(SUDOERS)))
async def get_weather(bot: Client, message: Message):
    if len(message.command) == 1:
        await message.edit("Usage: `.weather Maldives`")
        await asyncio.sleep(3)
        await message.delete()

    if len(message.command) > 1:
        location = message.command[1]
        headers = {"user-agent": "httpie"}
        url = f"https://wttr.in/{location}?mnTC0&lang=en"
        try:
            async with aiohttp.ClientSession(headers=headers) as session:
                async with session.get(url) as resp:
                    data = await resp.text()
        except Exception:
            await message.edit("Failed to get the weather forecast")

        if "we processed more than 1M requests today" in data:
            await message.edit("`Sorry, we cannot process this request today!`")
        else:
            weather = f"<code>{escape(data.replace('report', 'Report'))}</code>"
            await message.edit(weather, parse_mode=enums.ParseMode.MARKDOWN)


__NAME__ = "Wᴇᴀᴛʜᴇʀ"
__MENU__ = """
`.weather` - **Gets weather information for provided location..**
"""

