from pyrogram import Client, filters
from pyrogram.types import Message
from typing import Optional
from BADUC import SUDOERS
from BADUC.core.clients import app
from BADUC.core.command import *

# Dummy Database Implementation
class GreetingsDB:
    def __init__(self):
        self.welcome_text = "Welcome to the group!"

    def set_welcome_text(self, text: str, mtype: Optional[str] = None):
        self.welcome_text = text
        print(f"Welcome text set to: {text} | Type: {mtype}")

    def get_welcome_text(self) -> str:
        return self.welcome_text

# Initialize database
db = GreetingsDB()

# Define the command handler to set the welcome text
@app.on_message(filters.command("setwelcome") & filters.group)
async def set_welcome(client: Client, message: Message):
    try:
        if not message.reply_to_message:
            await message.reply("Please reply to a message containing the welcome text.")
            return
        
        # Get text from the replied message
        welcome_text = message.reply_to_message.text
        if not welcome_text:
            await message.reply("The replied message has no text!")
            return

        # Set the welcome text
        db.set_welcome_text(welcome_text, mtype="text")
        await message.reply(f"Welcome message has been set to:\n\n`{welcome_text}`")

    except Exception as e:
        print(f"Error: {e}")
        await message.reply("An error occurred while setting the welcome message.")

# Command to get the current welcome text
@app.on_message(filters.command("getwelcome") & filters.group)
async def get_welcome(client: Client, message: Message):
    try:
        welcome_text = db.get_welcome_text()
        await message.reply(f"The current welcome message is:\n\n`{welcome_text}`")

    except Exception as e:
        print(f"Error: {e}")
        await message.reply("An error occurred while fetching the welcome message.")
