import random
from pyrogram import Client, filters
from BADUC.core.clients import bot
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Group and Channel Links (Replace with actual links)
GROUP_LINK = "https://t.me/PBX_CHAT"  # Replace with your group link
CHANNEL_LINK = "https://t.me/HEROKUBIN_01"  # Replace with your channel link

# List of random images
IMAGE_LIST = [
    "https://files.catbox.moe/mpkdqt.jpg",
    "https://files.catbox.moe/wbog9f.jpg",
]

# Start command handler
@bot.on_message(filters.command("start") & filters.private)
async def start(client, message):
    random_image = random.choice(IMAGE_LIST)  # Pick a random image
    buttons = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("Assistant", callback_data="assistant")],
            [
                InlineKeyboardButton("Group Support", url=GROUP_LINK),
                InlineKeyboardButton("Channel Support", url=CHANNEL_LINK),
            ],
            [InlineKeyboardButton("Help", callback_data="help")],
            [InlineKeyboardButton("Clone", callback_data="clone")],
        ]
    )
    await client.send_photo(
        chat_id=message.chat.id,
        photo=random_image,
        caption="Welcome to the bot! Choose an option below:",
        reply_markup=buttons,
    )

# Callback query handler for Assistant
@bot.on_callback_query(filters.regex("assistant"))
async def assistant(client, callback_query):
    userbot_id = (await client.get_me()).id  # Get the bot's own ID
    await callback_query.message.edit_text(
        f"Userbot ID: `{userbot_id}`",
        reply_markup=None  # Remove buttons after showing the ID
    )

# Callback query handler for Help
@bot.on_callback_query(filters.regex("help"))
async def help(client, callback_query):
    help_text = (
        "**Help Menu**\n\n"
        "1. **Assistant**: Displays the Userbot ID.\n"
        "2. **Group Support**: Join the support group for assistance.\n"
        "3. **Channel Support**: Follow the updates in the channel.\n"
        "4. **Clone**: Automatically types the `/clone` command.\n"
        "5. For any issues, feel free to contact the support group."
    )
    await callback_query.message.edit_text(
        help_text,
        reply_markup=None  # Remove buttons after showing help
    )

# Callback query handler for Clone
@bot.on_callback_query(filters.regex("clone"))
async def clone(client, callback_query):
    await callback_query.message.reply_text("/clone")
    await callback_query.answer("Command sent to the chat!", show_alert=False)
