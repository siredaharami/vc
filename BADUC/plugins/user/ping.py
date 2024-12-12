from BADUC import SUDOERS
from BADUC.core.clients import app
from BADUC.core.command import *
from pyrogram import Client, filters
from pyrogram.types import Message
import aiohttp
import os
from datetime import datetime, timedelta


# Global Variables
PING_PIC = None
PING_TEMPLATE = """ﾠ╰•★★ 💫 🅿🅱🆇 2.0 💫 ★★•╯
❍════════════════════❍
╭✠╼━━━━━━❖━━━━━━━✠╮ 
│•**𝐒ᴘᴇᴇᴅ ➠** {speed} m/s
│•**𝐔ᴘᴛɪᴍᴇ ➠** {uptime}
│•**𝐎ᴡɴᴇʀ ➠** {owner} 
╰✠╼━━━━━━❖━━━━━━━✠╯
        ╔═════════════╗
            <b><i>✬  <a href='https://t.me/ll_THE_BAD_BOT_ll'> 🇨🇦  𝗣𝗕𝗫  🌸 </a>  ✬</i></b>
        ╚═════════════╝
❍════════════════════❍"""
START_TIME = datetime.now()

async def download_photo(url, filename):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    with open(filename, "wb") as file:
                        file.write(await response.read())
                    return filename
                else:
                    return None
    except Exception as e:
        print(f"Error downloading photo: {e}")
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
            if file_path and os.path.exists(file_path):
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
        
        if PING_PIC and os.path.exists(PING_PIC):
            await message.reply_photo(PING_PIC, caption=template)
        else:
            await message.reply_text(template)
    except Exception as e:
        await message.reply_text(f"❌ Error: {str(e)}")

