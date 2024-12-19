from pyrogram import Client, filters
from main import get_bot_owner  # Import the function to check bot owner

@Client.on_message(filters.command("ping"))
async def ping_command(client, message):
    bot_id = message.chat.id  # Get the current bot's ID
    user_id = message.from_user.id  # Get the user's ID

    # Check if the user is authorized to use this bot
    owner_id = await get_bot_owner(bot_id)
    if owner_id != user_id:
        await message.reply_text("❌ You're not authorized to use this bot.")
        return

    # If authorized, respond with a ping message
    await message.reply_text("🏓 Pong! The bot is responsive.")
