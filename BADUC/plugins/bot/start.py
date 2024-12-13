import random
from BADUC import SUDOERS
from BADUC.core.clients import bot
from BADUC.core.command import *
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton


# List of images for random selection
images = [
  "https://files.catbox.moe/qdueji.jpg",
  "https://files.catbox.moe/xkkllz.jpg",
  "https://files.catbox.moe/wbog9f.jpg",
]

# Welcome message handler
@bot.on_message(filters.command("start") & filters.private)
async def start(client, message):
    selected_image = random.choice(images)

    # Welcome text
    welcome_text = (
        "✨ **Welcome to My Dynamic Bot!** ✨\n\n"
        "🌟 This bot provides dynamic features and random content.\n"
        "Choose an option below to explore!"
    )

    # Inline keyboard with nested button options
    keyboard = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("🔍 Explore", callback_data="explore")],
            [InlineKeyboardButton("🗞 News", callback_data="news")],
            [
                InlineKeyboardButton("📊 Stats", callback_data="stats"),
                InlineKeyboardButton("ℹ️ Help", callback_data="help"),
            ],
        ]
    )

    # Send a message with a random image and buttons
    await message.reply_photo(
        photo=selected_image,
        caption=welcome_text,
        reply_markup=keyboard,
    )


# Callback query handler for buttons
@bot.on_callback_query()
async def handle_callback_query(client, callback_query):
    data = callback_query.data

    # Predefined responses for each button
    if data == "explore":
        response_text = "🔍 **Explore Options:**\n\n1. Feature A\n2. Feature B\n3. Feature C"
    elif data == "news":
        response_text = "🗞 **Latest News:**\n\n- News Item 1\n- News Item 2\n- News Item 3"
    elif data == "stats":
        response_text = "📊 **Statistics:**\n\n- Stat A: 100\n- Stat B: 200"
    elif data == "help":
        response_text = "ℹ️ **Help Section:**\n\nContact us at @support"
    else:
        response_text = "❓ Unknown option. Please try again."

    # Updated inline keyboard for nested navigation
    updated_keyboard = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("⬅️ Back", callback_data="back")],
        ]
    )

    # Edit the same message with the new content
    await callback_query.message.edit_text(
        text=response_text, reply_markup=updated_keyboard
    )

    # Handle the "Back" button
    if data == "back":
        # Reset to the initial message and buttons
        selected_image = random.choice(images)
        initial_text = (
            "✨ **Welcome to My Dynamic Bot!** ✨\n\n"
            "🌟 This bot provides dynamic features and random content.\n"
            "Choose an option below to explore!"
        )

        initial_keyboard = InlineKeyboardMarkup(
            [
                [InlineKeyboardButton("🔍 Explore", callback_data="explore")],
                [InlineKeyboardButton("🗞 News", callback_data="news")],
                [
                    InlineKeyboardButton("📊 Stats", callback_data="stats"),
                    InlineKeyboardButton("ℹ️ Help", callback_data="help"),
                ],
            ]
        )

        # Update the message with a new random image and buttons
        await callback_query.message.edit_media(
            media={"type": "photo", "media": selected_image},
            caption=initial_text,
            reply_markup=initial_keyboard,
        )
