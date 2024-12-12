import os
from BADUC import SUDOERS
from BADUC.core.clients import app
from pyrogram import Client, filters
from pyrogram.types import Message
from datetime import datetime

# Global Variables
ALIVE_PIC = "https://files.catbox.moe/ntb52f.jpg"  # Default Alive Picture
ALIVE_TEMPLATES = [
    (
        "╰•★★ 💫 𝐁ᴀᴅ 𝐔ꜱᴇʀ 𝐁ᴏᴛ 𝐀ʟɪᴠᴇ💫 ★★•╯\n"
        "❍═════════════════════════❍\n\n"
        "╭✠╼━━━━━━❖━━━━━━━✠╮\n"
        "│➠ 𝐎ᴡɴᴇʀ » {owner}\n"
        "│➠ 𝐏ʏʀᴏɢʀᴀᴍ » {pyrogram}\n"
        "│➠ 𝐁ᴀᴅᴜꜱᴇʀʙᴏᴛ » {Pbxbot}\n"
        "│➠ 𝐏ʏᴛʜᴏɴ » {python}\n"
        "│➠ 𝐔ᴘᴛɪᴍᴇ » {uptime}\n"
        "╰✠╼━━━━━━❖━━━━━━━✠╯\n\n"
        "     ╔═════════════╗\n"
        "              [ 🇨🇦  𝗕𝗔𝗗  🌸 ](https://t.me/ll_THE_BAD_BOT_ll)\n"
        "     ╚═════════════╝\n\n"
        "❍═════════════════════════❍\n"
    ),
]
current_template = 0  # Default template index

# Commands
@app.on_message(bad(["alive"]) & (filters.me | filters.user(SUDOERS)))
async def alive(_, message: Message):
    owner = message.from_user.first_name if message.from_user else "Unknown"
    uptime = datetime.now().strftime("%H:%M:%S, %d-%m-%Y")
    pyrogram_version = "2.0.106"
    python_version = "3.9"
    pbxbot_version = "2.0"

    text = ALIVE_TEMPLATES[current_template].format(
        owner=owner,
        pyrogram=pyrogram_version,
        python=python_version,
        Pbxbot=pbxbot_version,
        uptime=uptime,
    )
    
    await app.send_photo(
        message.chat.id,
        photo=ALIVE_PIC,
        caption=text,
    )


@app.on_message(bad(["setvar"]) & (filters.me | filters.user(SUDOERS)))
async def set_variable(_, message: Message):
    global ALIVE_PIC
    global current_template
    
    if len(message.command) < 3:
        await message.reply_text("Usage: `.setvar VARIABLE VALUE`")
        return

    variable, value = message.command[1], " ".join(message.command[2:])
    
    if variable.upper() == "ALIVE_PIC":
        ALIVE_PIC = value
        await message.reply_text(f"✅ ALIVE_PIC updated to: {value}")
    elif variable.upper() == "ALIVE_TEMPLATE":
        try:
            template_index = int(value)
            if 0 <= template_index < len(ALIVE_TEMPLATES):
                current_template = template_index
                await message.reply_text(f"✅ Template updated to index {template_index}.")
            else:
                await message.reply_text("❌ Invalid template index.")
        except ValueError:
            await message.reply_text("❌ Template index must be an integer.")
    else:
        await message.reply_text("❌ Unknown variable. Only `ALIVE_PIC` or `ALIVE_TEMPLATE` are supported.")
          
