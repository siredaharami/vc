from BADUC import SUDOERS
from BADUC.core.clients import app
from BADUC.core.command import *
from pymongo import MongoClient
import os
from pyrogram import Client, filters
from pyrogram.types import Message
from datetime import datetime
import time

# MongoDB Setup
MONGO_URL = os.getenv("MONGO_URL", "mongodb+srv://BADMUNDA:BADMYDAD@badhacker.i5nw9na.mongodb.net/")
client = MongoClient(MONGO_URL)
db = client["baduserbot"]
config_collection = db["config"]

# Default Variables
default_config = {
    "ALIVE_PIC": "https://files.catbox.moe/ntb52f.jpg",
    "PING_PIC": "https://files.catbox.moe/83d5lc.jpg",
    "ALIVE_TEMPLATE_INDEX": 0,
    "PING_TEMPLATE_INDEX": 0,
}

# Load Config from MongoDB or Use Defaults
config = config_collection.find_one({"_id": "config"}) or default_config
ALIVE_PIC = config.get("ALIVE_PIC")
PING_PIC = config.get("PING_PIC")
current_template = config.get("ALIVE_TEMPLATE_INDEX")
current_ping_template = config.get("PING_TEMPLATE_INDEX")

# Templates
ALIVE_TEMPLATES = [
    (
        "  ╰•★★ 💫 𝐁ᴀᴅ 𝐔ꜱᴇʀ 𝐁ᴏᴛ 𝐀ʟɪᴠᴇ 💫 ★★•╯\n"
        "❍═════════════════════════❍\n\n"
        "╭✠╼━━━━━━❖━━━━━━━✠╮\n"
        "│➠ 𝐎ᴡɴᴇʀ » {owner}\n"
        "│➠ 𝐏ʏʀᴏɢʀᴀᴍ » {pyrogram}\n"
        "│➠ 𝐏ʙxʙᴏᴛ 2.0 » {baduserbot}\n"
        "│➠ 𝐏ʏᴛʜᴏɴ » {python}\n"
        "│➠ 𝐔ᴘᴛɪᴍᴇ » {uptime}\n"
        "╰✠╼━━━━━━❖━━━━━━━✠╯\n\n"
        "     ╔═════════════╗\n"
        "              [ 🇨🇦 𝗕𝗔𝗗  🌸 ](https://t.me/HEROKUBIN_01)\n"
        "     ╚═════════════╝\n\n"
        "❍═════════════════════════❍\n"
    ),
]

PING_TEMPLATE = [
    """╰•★★ 💫 𝐁ᴀᴅ 𝐔ꜱᴇʀ𝐁ᴏᴛ 💫 ★★•╯
❍════════════════════❍
╭✠╼━━━━━━❖━━━━━━━✠╮ 
│•**𝐒ᴘᴇᴇᴅ ➠** {speed} m/s
│•**𝐔ᴘᴛɪᴍᴇ ➠** {uptime}
│•**𝐎ᴡɴᴇʀ ➠** {owner} 
╰✠╼━━━━━━❖━━━━━━━✠╯
        ╔═════════════╗
            <b><i>✬  <a href='https://t.me/HEROKUBIN_01'> 🇨🇦  𝗕𝗔𝗗  🌸 </a>  ✬</i></b>
        ╚═════════════╝

❍════════════════════❍""",
]

# Commands
@app.on_message(bad(["alive"]) & (filters.me | filters.user(SUDOERS)))
async def alive(_, message: Message):
    owner = message.from_user.first_name if message.from_user else "Unknown"
    uptime = datetime.now().strftime("%H:%M:%S, %d-%m-%Y")
    pyrogram_version = "2.0.106"
    python_version = "3.9"
    baduserbot_version = "2.0"

    text = ALIVE_TEMPLATES[current_template].format(
        owner=owner,
        pyrogram=pyrogram_version,
        python=python_version,
        baduserbot=baduserbot_version,
        uptime=uptime,
    )
    
    await app.send_photo(
        message.chat.id,
        photo=ALIVE_PIC,
        caption=text,
    )

@app.on_message(bad(["ping"]) & (filters.me | filters.user(SUDOERS)))
async def ping(_, message: Message):
    owner = message.from_user.first_name if message.from_user else "Unknown"
    start_time = time.time()
    uptime = datetime.now().strftime("%H:%M:%S, %d-%m-%Y")
    
    speed = round(1 / (time.time() - start_time), 2)  # Calculating speed
    text = PING_TEMPLATE[current_ping_template].format(speed=speed, uptime=uptime, owner=owner)

    await app.send_photo(
        message.chat.id,
        photo=PING_PIC,
        caption=text,
    )

@app.on_message(bad(["setvar"]) & (filters.me | filters.user(SUDOERS)))
async def set_variable(_, message: Message):
    global ALIVE_PIC, PING_PIC, current_template, current_ping_template
    
    if len(message.command) < 3:
        await message.reply_text("Usage: `.setvar VARIABLE VALUE`")
        return

    variable, value = message.command[1], " ".join(message.command[2:])
    if variable.upper() == "ALIVE_PIC":
        ALIVE_PIC = value
        config_collection.update_one({"_id": "config"}, {"$set": {"ALIVE_PIC": value}}, upsert=True)
        await message.reply_text(f"✅ ALIVE_PIC updated to: {value}")
    elif variable.upper() == "PING_PIC":
        PING_PIC = value
        config_collection.update_one({"_id": "config"}, {"$set": {"PING_PIC": value}}, upsert=True)
        await message.reply_text(f"✅ PING_PIC updated to: {value}")
    elif variable.upper() == "ALIVE_TEMPLATE":
        try:
            template_index = int(value)
            if 0 <= template_index < len(ALIVE_TEMPLATES):
                current_template = template_index
                config_collection.update_one({"_id": "config"}, {"$set": {"ALIVE_TEMPLATE_INDEX": template_index}}, upsert=True)
                await message.reply_text(f"✅ Template updated to index {template_index}.")
            else:
                await message.reply_text("❌ Invalid template index.")
        except ValueError:
            await message.reply_text("❌ Template index must be an integer.")
    elif variable.upper() == "PING_TEMPLATE":
        try:
            template_index = int(value)
            if 0 <= template_index < len(PING_TEMPLATE):
                current_ping_template = template_index
                config_collection.update_one({"_id": "config"}, {"$set": {"PING_TEMPLATE_INDEX": template_index}}, upsert=True)
                await message.reply_text(f"✅ Ping template updated to index {template_index}.")
            else:
                await message.reply_text("❌ Invalid ping template index.")
        except ValueError:
            await message.reply_text("❌ Ping template index must be an integer.")
    else:
        await message.reply_text("❌ Unknown variable. Only `ALIVE_PIC`, `PING_PIC`, `ALIVE_TEMPLATE`, or `PING_TEMPLATE` are supported.")
