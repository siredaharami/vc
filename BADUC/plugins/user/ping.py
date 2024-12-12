from BADUC import SUDOERS
from BADUC.core.clients import app
from pyrogram import Client, filters
from pyrogram.types import Message
import aiohttp
import os
from datetime import datetime, timedelta


# Global Variables
PING_PIC = None
PING_TEMPLATE = """ﾠ╰•★★ 💫 𝐁ᴀᴅ 𝐔ꜱᴇʀ 𝐁ᴏᴛ 💫 ★★•╯
❍════════════════════❍
╭✠╼━━━━━━❖━━━━━━━✠╮ 
│•**𝐒ᴘᴇᴇᴅ ➠** {speed} m/s
│•**𝐔ᴘᴛɪᴍᴇ ➠** {uptime}
│•**𝐎ᴡɴᴇʀ ➠** {owner} 
╰✠╼━━━━━━❖━━━━━━━✠╯
❍════════════════════❍"""
START_TIME = datetime.now()

async def download_photo(url, filename):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                with open(filename, "wb") as file:
                    file.write(await response.read())
                return filename
            return None

@app.on_message(bad(["setvar"]) & (filters.me | filters.user(SUDOERS)))
async def set_variable(client: Client, message: Message):
    global PING_PIC, PING_TEMPLATE
    try:
        command = message.text.split(maxsplit=2)
        if len(command) < 3:
            await message.reply_text("❌ Invalid format. Use `.setvar PING_PIC (photo URL)` or `.setvar PING_TEMPLATE (template)`.")
            return

        key, value = command[1].upper(), command[2]
        if key == "PING_PIC":
            filename = "ping_pic.jpg"
            file_path = await download_photo(value, filename)
            if file_path:
                PING_PIC = file_path
                await message.reply_text("✅ Ping photo has been set!")
            else:
                await message.reply_text("❌ Failed to download the photo. Check the URL.")
        elif key == "PING_TEMPLATE":
            PING_TEMPLATE = value
            await message.reply_text("✅ Ping template has been updated!")
        else:
            await message.reply_text("❌ Invalid key. Use `PING_PIC` or `PING_TEMPLATE`.")
    except Exception as e:
        await message.reply_text(f"❌ Error: {str(e)}")

@app.on_message(bad(["ping"]) & (filters.me | filters.user(SUDOERS)))
async def ping_command(client: Client, message: Message):
    global PING_PIC, PING_TEMPLATE
    try:
        speed = round((datetime.now() - message.date).total_seconds() * 1000, 2)
        uptime = str(timedelta(seconds=(datetime.now() - START_TIME).total_seconds()))
        owner = message.from_user.first_name if message.from_user else "Unknown"
        template = PING_TEMPLATE.format(speed=speed, uptime=uptime, owner=owner)
        
        if PING_PIC:
            await message.reply_photo(PING_PIC, caption=template)
        else:
            await message.reply_text(template)
    except Exception as e:
        await message.reply_text(f"❌ Error: {str(e)}")
        
