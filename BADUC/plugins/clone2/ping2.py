from pyrogram import filters
from datetime import datetime
from BADUC.plugins.bot.app import app

@app.on_message(filters.command("pingg"))
async def ping(client, message):
    start_time = datetime.now()
    response = await message.reply_text("**Pinging...**")
    end_time = datetime.now()
    ping_time = (end_time - start_time).microseconds / 1000  # Convert to milliseconds
    await response.edit_text(f"**Pong!** 🏓\n`{ping_time} ms`")
