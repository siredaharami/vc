from pyrogram import Client, filters
from BADUC.plugins.bot.clone3 import get_bot_owner  # Import the function to check bot owner
from BADUC.plugins.clone2.help import *
# Function to register this plugin
def register_plugin(plugin_details):
    plugin_details["ping"] = """
**Ping Plugin**
- **Command**: /ping
- **Description**: Checks the bot's latency.
"""
    
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

    # If authorized, respond with a ping message
    await message.reply_text("🏓 Pong! The bot is responsive.")
