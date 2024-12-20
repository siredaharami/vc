from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import time
import psutil
from BADUC.plugins.bot.clone3 import get_bot_owner  # Import the function to check bot owner

@Client.on_message(filters.command("ping"))
async def ping_command(client, message):
    bot_info = await client.get_me()  # Retrieve current bot's details
    bot_id = bot_info.id  # Get the current bot's ID
    user_id = message.from_user.id  # Get the user's ID

    # Check if the user is authorized to use this bot
    owner_id = await get_bot_owner(bot_id)
    if owner_id != user_id:
        await message.reply_text("❌ You're not authorized to use this bot.")
        return

    # Measure the ping speed
    start_time = time.time()
    pong = await message.reply_text("🏓 Pong! Checking ping...")
    ping_time = round((time.time() - start_time) * 1000)  # Convert to milliseconds

    # Calculate uptime
    uptime_seconds = int(time.time() - psutil.boot_time())
    uptime = f"{uptime_seconds // 3600}h {((uptime_seconds % 3600) // 60)}m"

    # Get the bot owner (for example, username)
    owner = await client.get_users(owner_id)
    owner_name = owner.username if owner.username else "Unknown"

    # Prepare the message in the desired format
    ping_text = f"""
    ╭✠╼━━━━━━❖━━━━━━━✠╮
    │•**𝐒ᴘᴇᴇᴅ ➠** {ping_time}ms
    │•**𝐔ᴘᴛɪᴍᴇ ➠** {uptime}
    │•**𝐎ᴡɴᴇʀ ➠** @{owner_name}
    ╰✠╼━━━━━━❖━━━━━━━✠╯
    """

    # Prepare the buttons for Support and Update
    support_button = InlineKeyboardButton("ꜱᴜᴘᴘᴏʀᴛ", url="https://t.me/PBX_CHAT")
    update_button = InlineKeyboardButton("ᴜᴘᴅᴀᴛᴇ", url="https://t.me/HEROKUBIN_01")
    buttons = InlineKeyboardMarkup([[support_button, update_button]])

    # Update the message with the ping details and buttons
    await pong.edit_text(ping_text, reply_markup=buttons)
