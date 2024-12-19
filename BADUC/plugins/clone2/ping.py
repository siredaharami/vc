from BADUC.core.clients import bot
from pyrogram import Client, filters
from datetime import datetime

# Ping command ka handler
@Client.on_message(filters.command("ping"))
async def ping_command(client, message):
    start_time = datetime.now()  # Start time
    response = await message.reply_text("🏓 Pong!")
    end_time = datetime.now()  # End time
    latency = (end_time - start_time).microseconds / 1000  # Milliseconds me latency calculate karein
    await response.edit_text(f"🏓 Pong!\n**Latency:** `{latency} ms`")
