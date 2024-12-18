import random
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from BADUC.core.clients import bot, app  # Import bot and app
from BADUC.core.config import OWNER_ID  # Import OWNER_ID from config

# Group and Channel Links (Replace with actual links)
GROUP_LINK = "https://t.me/PBX_CHAT"
CHANNEL_LINK = "https://t.me/HEROKUBIN_01"

# Random images list
IMAGE_LIST = [
    "https://files.catbox.moe/mpkdqt.jpg",
    "https://files.catbox.moe/wbog9f.jpg",
]

# Start command handler
@bot.on_message(filters.command("start") & filters.private)
async def start(client, message):
    random_image = random.choice(IMAGE_LIST)

    # Fetch the bot's username or ID dynamically
    assistant_info = await client.get_me()
    assistant_id = assistant_info.username or assistant_info.id

    # Fetch the owner's username or numeric ID
    owner_info = await app.get_users(OWNER_ID)
    owner_username = owner_info.username or OWNER_ID

    buttons = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("Assistant ID", url=f"https://t.me/{assistant_id}"),
                InlineKeyboardButton("Owner ID", url=f"https://t.me/{owner_username}"),
            ],
            [
                InlineKeyboardButton("Clone Menu", callback_data="clone"),
                InlineKeyboardButton("Group", url=GROUP_LINK),
                InlineKeyboardButton("Channel", url=CHANNEL_LINK),
            ],
        ]
    )
    await client.send_photo(
        chat_id=message.chat.id,
        photo=random_image,
        caption="Welcome! Choose an option below:",
        reply_markup=buttons,
    )

# Callback query handler for Clone
@bot.on_callback_query(filters.regex("clone"))
async def clone_menu(client, callback_query):
    buttons = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("Bot Clone", callback_data="bot_clone")],
            [InlineKeyboardButton("Userbot Clone", callback_data="userbot_clone")],
            [InlineKeyboardButton("Session Clone", callback_data="string_session")],
        ]
    )
    await callback_query.message.edit_text(
        "Clone options are displayed below:",
        reply_markup=buttons,
    )
    await callback_query.answer("Clone menu opened!")

# Callback query handler for Bot Clone
@bot.on_callback_query(filters.regex("bot_clone"))
async def bot_clone(client, callback_query):
    await callback_query.message.edit_text(
        "Bot Clone: Instructions for cloning bots will appear here.",
        reply_markup=None,
    )
    await callback_query.answer("Bot Clone info displayed!")

# Callback query handler for Userbot Clone
@bot.on_callback_query(filters.regex("userbot_clone"))
async def userbot_clone(client, callback_query):
    await callback_query.message.edit_text(
        "Userbot Clone: Instructions for cloning userbots will appear here.",
        reply_markup=None,
    )
    await callback_query.answer("Userbot Clone info displayed!")

# Callback query handler for String Session Clone
@bot.on_callback_query(filters.regex("string_session"))
async def string_session_handler(client, callback_query):
    # Automatically fetch and display the session string using `app`
    async with app:
        string_session = app.export_session_string()
    
    await callback_query.message.edit_text(
        f"Here is your String Session:\n\n`{string_session}`",
        reply_markup=None,
    )
    await callback_query.answer("String session generated!")
    
