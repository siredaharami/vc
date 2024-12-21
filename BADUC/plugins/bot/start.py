from pyrogram import Client, filters
from BADUC.core.clients import bot
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

# Photo URLs for Start Command
start_photos = [
    "https://files.catbox.moe/zh4g9l.jpg",
    "https://files.catbox.moe/mi2asx.jpg",
    "https://files.catbox.moe/wxlgwq.jpg"
]
current_photo = 0  # To track the current photo index

async def get_next_photo():
    global current_photo
    photo = start_photos[current_photo]
    current_photo = (current_photo + 1) % len(start_photos)
    return photo

# Start Command
@bot.on_message(filters.command("start"))
async def start(bot, message):
    # Buttons with text
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("owner", url="https://your-repo-link.com")],
        [InlineKeyboardButton("Repo", url="https://your-repo-link.com"),
         InlineKeyboardButton("Support", url="https://your-support-link.com")],
        [InlineKeyboardButton("Update", url="https://your-update-link.com"),
         InlineKeyboardButton("Help", callback_data="help")]
    ])
    photo = await get_next_photo()
    caption = (
        "👋 **Welcome to the Bot!**\n\n"
        "📚 **Features:**\n"
        "- Explore the Repo.\n"
        "- Join Support and Update channels.\n"
        "- Get Help for various options.\n\n"
        "🔘 **Click the buttons below to proceed.**"
    )
    await message.reply_photo(photo, caption=caption, reply_markup=keyboard)

# Callback Query Handler
@bot.on_callback_query()
async def callback_query_handler(bot, query):
    if query.data == "help":
        # Help Menu Buttons
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("Game", callback_data="game"),
             InlineKeyboardButton("Clone", callback_data="clone")],
            [InlineKeyboardButton("String Session", url="https://your-string-session-link.com")]
        ])
        await query.message.edit_text(
            "📖 **Help Menu**\n\n"
            "1️⃣ **Game**: Instructions for the game.\n"
            "2️⃣ **Clone**: How to use cloning features.\n"
            "3️⃣ **String Session**: Generate a string session easily.\n\n"
            "🔘 **Click the buttons below to proceed.**",
            reply_markup=keyboard
        )

    elif query.data == "game":
        # Game Text with Back Button
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("Back", callback_data="help")]
        ])
        await query.message.edit_text(
            "🎮 **Game Instructions:**\n\n"
            "Learn how to play the game here!\n\n"
            "🔙 **Click 'Back' to return to the Help Menu.**",
            reply_markup=keyboard
        )

    elif query.data == "clone":
        # Clone Text with Back Button
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("Back", callback_data="help")]
        ])
        await query.message.edit_text(
            "📦 **Clone Instructions:**\n\n"
            "Learn how to use cloning features here!\n\n"
            "🔙 **Click 'Back' to return to the Help Menu.**",
            reply_markup=keyboard
        )
