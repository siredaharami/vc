from pyrogram import Client, filters
import time
from BADUC.core.clients import app

@app.on_message(filters.command("ping") & filters.private)
async def ping(client, message):
    start_time = time.time()  # Start time to calculate latency
    sent_message = await message.reply("Pinging...")  # Initial reply
    end_time = time.time()  # End time after message is sent

    latency = (end_time - start_time) * 1000  # Convert seconds to milliseconds

    # Big Ping Message
    big_ping_message = f"""
<b>PONG! 🏓</b>

<b>🏠 Server:</b> Pyrogram Userbot
<b>📡 Latency:</b> <code>{latency:.2f} ms</code>
<b>⚡ API Response:</b> Alive & Active
<b>🌐 Server Time:</b> {time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime())}

<b>💻 Powered by:</b> Pyrogram
<b>🔗 GitHub:</b> https://github.com/pyrogram/pyrogram

Stay Connected!
"""
    await sent_message.edit_text(big_ping_message, parse_mode="html")

