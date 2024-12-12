from pyrogram import Client, filters
from BADUC.core.clients import bot
from BADUC.core.command import *

# Start command handler
@bot.on_message(bad(["start"]))
def start(client, message):
    message.reply_text(
        f"Hello {message.from_user.first_name}!\n"
        "I am your bot, here to assist you. Type /help to see what I can do!"
    )
