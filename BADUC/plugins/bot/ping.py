from pyrogram import Client, filters
from .. import bot
import time


@bot.on_message(cdx(["help"]))
async def ping_command(client, message):
    start_time = time.time()  # Start time to calculate latency
    sent_message = await message.reply("Pinging... 🏓")  # Initial reply
    end_time = time.time()  # End time after message is sent

    latency = (end_time - start_time) * 1000  # Convert seconds to milliseconds

    # Detailed Ping Message
    ping_message = f"""
<b>🏓 PONG! Bot is Alive!</b>

<b>📡 Latency:</b> <code>{latency:.2f} ms</code>
<b>🌐 Server Time:</b> {time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime())}
<b>🔗 Pyrogram Version:</b> {client.__version__}

<b>🤖 Bot Status:</b> Online & Active
<b>💻 Hosted By:</b> Your Bot Name
<b>🛠️ Powered By:</b> Python & Pyrogram

Enjoy your day! 😊
"""
    await sent_message.edit_text(ping_message, parse_mode="html")

