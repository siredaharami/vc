from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import random
import os

# Replace with the bot instance and owner/assistant details
from BADUC.core.clients import bot
from BADUC.core.command import *

# List of start image URLs
START_IMAGES = [
    "https://files.catbox.moe/mpkdqt.jpg",  
    "https://files.catbox.moe/wbog9f.jpg",  
    "https://files.catbox.moe/abcd123.jpg"   # Example image
]

# Config placeholders
ASSISTANT_ID = "https://t.me/II_BAD_BABY_II"  # Telegram link to the assistant
SESSION_LINK = "https://telegram.tools/session-string-generator#pyrogram,user"
OWNER_USERNAME = "https://t.me/II_BAD_BABY_II"


# Start command handler
@bot.on_message(filters.command("start"))
async def start(client, message):
    try:
        # Randomly select an image
        selected_image = random.choice(START_IMAGES)

        # Keyboard layout
        keyboard = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("BADUSERBOT", callback_data="baduserbot"),
                InlineKeyboardButton("Group Support", url="https://t.me/support_group"),
            ],
            [
                InlineKeyboardButton("Channel Update", url="https://t.me/your_channel"),
            ]
        ])

        # Send the response with a random image
        await message.reply_photo(
            photo=selected_image,
            caption=(
                "Welcome to the Bot! Here are some details:\n\n"
                f"**Userbot Version**: 1.0.0\n"
                f"**Python Version**: {os.sys.version.split()[0]}\n"
                f"**Pytgcalls Version**: 1.1.1\n"
                f"**Pyrogram Version**: 1.2.0"
            ),
            reply_markup=keyboard
        )

    except Exception as e:
        # Log the error and notify the user
        print(f"Error in start command: {e}")
        await message.reply("An error occurred while processing your request. Please try again later.")


# Callback query handler
@bot.on_callback_query()
async def callback_query(client, callback_query):
    data = callback_query.data

    try:
        # Handle the BADUSERBOT button click
        if data == "baduserbot":
            keyboard = InlineKeyboardMarkup([
                [
                    InlineKeyboardButton("Assistant", url=ASSISTANT_ID),  # Opens the assistant's link
                    InlineKeyboardButton("BOT OWNER", callback_data="bot_owner"),
                ],
                [
                    InlineKeyboardButton("CLONE", callback_data="clone"),
                ]
            ])
            await callback_query.message.edit_text(
                "Choose an option:",
                reply_markup=keyboard
            )

        # Handle the BOT OWNER button click
        elif data == "bot_owner":
            await callback_query.message.edit_text(f"Contact the bot owner: @{OWNER_USERNAME}")

        # Handle the CLONE button click
        elif data == "clone":
            keyboard = InlineKeyboardMarkup([
                [
                    InlineKeyboardButton("Bot Clone", callback_data="bot_clone"),
                    InlineKeyboardButton("Session Clone", callback_data="session_clone"),
                    InlineKeyboardButton("String Generate", url=SESSION_LINK),
                ]
            ])
            await callback_query.message.edit_text(
                "Select cloning option:",
                reply_markup=keyboard
            )

        # Handle the Bot Clone button click
        elif data == "bot_clone":
            await callback_query.message.edit_text("Please type the bot cloning details.")

        # Handle the Session Clone button click
        elif data == "session_clone":
            await callback_query.message.edit_text("Please type the session cloning details.")

    except Exception as e:
        # Log callback handling errors
        print(f"Error in callback query: {e}")
        await callback_query.answer("An error occurred while processing your request.", show_alert=True)
