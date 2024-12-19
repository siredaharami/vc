from BADUC.core.clients import bot
from BADUC.core.config import API_ID, API_HASH, BOT_TOKEN
from pyrogram import Client, filters
from pyrogram.types import Message

@bot.on_message(filters.command("clone"))
async def clone(bot, msg: Message):
    if len(msg.command) < 2:
        await msg.reply("Usage: `/clone <session_name>`\n\nReplace `<session_name>` with the desired name for the cloned session.")
        return

    session_name = msg.command[1]  # Get the session name from the command
    response = await msg.reply("Initializing your bot client...")

    try:
        # Initialize and start a new Pyrogram bot client
        client = Client(
            name=session_name,
            api_id=API_ID,
            api_hash=API_HASH,
            bot_token=BOT_TOKEN,
            plugins=dict(root="BADUC/plugins/clone2")  # Adjust the plugins path if needed
        )
        await client.start()
        bot_info = await client.get_me()  # Get bot details

        await response.edit(f"Your bot client has been successfully initialized as **{bot_info.first_name}** ✅.")
    except Exception as e:
        await response.edit(f"**ERROR:** `{str(e)}`\n\nPlease check your configuration and try again.")
