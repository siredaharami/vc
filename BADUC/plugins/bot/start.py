import random
from pyrogram import Client, filters
from BADUC.core.clients import bot  # Import your custom bot instance
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from BADUC.core.config import OWNER_ID  # Import OWNER_ID from config


from BADUC.core.clients import app as session_string  

# Group and Channel Links (Replace with actual links)
GROUP_LINK = "https://t.me/PBX_CHAT"
CHANNEL_LINK = "https://t.me/HEROKUBIN_01"

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
            [InlineKeyboardButton("Help", callback_data="help")],
            [InlineKeyboardButton("Clone", callback_data="clone")],
            [InlineKeyboardButton("Group Link", url=GROUP_LINK)],
            [InlineKeyboardButton("Channel Link", url=CHANNEL_LINK)],
            [InlineKeyboardButton("Owner", callback_data="owner")],
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
    string_session = session_string.save(client.session)  # Get the string session
    await callback_query.message.edit_text(
        f"Here is your Bot's String Session:\n\n`{string_session}`",
        reply_markup=None  # Remove buttons after showing the session ID
    )
    await callback_query.answer("String session displayed!")

# Callback query handler for Help
@bot.on_callback_query(filters.regex("help"))
async def help(client, callback_query):
    help_text = (
        "**Help Menu**\n\n"
        "1. **Assistant**: Displays the Bot's String Session.\n"
        "2. **Help**: Displays this menu.\n"
        "3. **Clone**: Displays options to clone bots."
    )
    await callback_query.message.edit_text(
        help_text,
        reply_markup=None  # Remove buttons after showing help
    )
    await callback_query.answer("Help menu displayed!")

# Callback query handler for Clone
@bot.on_callback_query(filters.regex("clone"))
async def clone(client, callback_query):
    buttons = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("Bot Clone", callback_data="bot_clone")],
            [InlineKeyboardButton("Userbot Clone", callback_data="userbot_clone")],
            [InlineKeyboardButton("String Session", callback_data="string_session")],
        ]
    )
    await callback_query.message.edit_text(
        "Choose the clone option below:",
        reply_markup=buttons
    )
    await callback_query.answer("Clone options are displayed!")

# Callback query handler for Bot Clone
@bot.on_callback_query(filters.regex("bot_clone"))
async def bot_clone(client, callback_query):
    await callback_query.message.edit_text(
        "Bot has been cloned successfully!\n\n(For demo purposes, this is a placeholder message.)",
        reply_markup=None
    )
    await callback_query.answer("Bot cloned!")

# Callback query handler for Userbot Clone
@bot.on_callback_query(filters.regex("userbot_clone"))
async def userbot_clone(client, callback_query):
    await callback_query.message.edit_text(
        "Userbot has been cloned successfully!\n\n(For demo purposes, this is a placeholder message.)",
        reply_markup=None
    )
    await callback_query.answer("Userbot cloned!")

# Callback query handler for String Session
@bot.on_callback_query(filters.regex("string_session"))
async def string_session(client, callback_query):
    string_session = session_string.save(client.session)  # Get the string session
    await callback_query.message.edit_text(
        f"Here is your Bot's String Session:\n\n`{string_session}`",
        reply_markup=None  # Remove buttons after showing the session ID
    )
    await callback_query.answer("String session displayed!")

# Callback query handler for Owner
@bot.on_callback_query(filters.regex("owner"))
async def owner(client, callback_query):
    await callback_query.message.edit_text(
        f"Bot Owner ID: `{OWNER_ID}`",  # Display the Owner ID from the config
        reply_markup=None  # Remove buttons after showing the owner ID
    )
    await callback_query.answer("Owner ID displayed!")

