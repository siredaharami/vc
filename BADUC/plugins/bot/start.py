from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import random
import os

from BADUC.core.clients import *
from BADUC.core.config import OWNER_ID
from BADUC.core.command import *

# List of start image URLs
START_IMAGES = [
    "https://files.catbox.moe/mpkdqt.jpg",  # Replace with actual image URLs
    "https://files.catbox.moe/wbog9f.jpg",  # Replace with actual image URLs
    "https://files.catbox.moe/wbog9f.jpg"   # Replace with actual image URLs
]

# Config file (you can import the necessary details from a configuration file)
ASSISTANT_ID = "@II_BAD_BABY_II"
SESSION_LINK = "https://telegram.tools/session-string-generator#pyrogram,user"

# Start command handler
@app.on_message(filters.command("start"))
async def start(client, message):
    # Randomly select an image URL for the start message
    selected_image = random.choice(START_IMAGES)
    
    # Create the keyboard with the buttons
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("BADUSERBOT", callback_data="baduserbot"),
         InlineKeyboardButton("Group Support", url="https://t.me/support_group")],
        [InlineKeyboardButton("Channel Update", url="https://t.me/your_channel")]
    ])
    
    # Send start message with image URL and bot versions
    await message.reply_photo(
        photo=selected_image,
        caption=f"Welcome to the Bot! Here are the details:\n\n"
                f"Userbot Version: 1.0.0\nPython Version: {os.sys.version}\n"
                f"Pytgcalls Version: 1.1.1\nPyrogram Version: 1.2.0",
        reply_markup=keyboard
    )

# Callback query handler for buttons
@app.on_callback_query()
async def callback_query(client, callback_query):
    data = callback_query.data
    
    # Handle the BADUSERBOT button click
    if data == "baduserbot":
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("ASSISTANT ID", callback_data="assistant_id"),
             InlineKeyboardButton("BOT OWNER", callback_data="bot_owner"),
             InlineKeyboardButton("CLONE", callback_data="clone")]
        ])
        await callback_query.message.edit_text(
            "Choose an option:",
            reply_markup=keyboard
        )
    
    # Handle the ASSISTANT ID button click
    elif data == "assistant_id":
        await callback_query.message.edit_text(f"Assistant ID: {ASSISTANT_ID}")
    
    # Handle the BOT OWNER button click
    elif data == "bot_owner":
        await callback_query.message.edit_text(f"Contact the bot owner: @{OWNER_ID}")
    
    # Handle the CLONE button click
    elif data == "clone":
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("Bot Clone", callback_data="bot_clone"),
             InlineKeyboardButton("Session Clone", callback_data="session_clone"),
             InlineKeyboardButton("String Generate", url=SESSION_LINK)]
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
      
