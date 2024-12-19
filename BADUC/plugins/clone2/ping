from pyrogram import Client, filters
from pyrogram.types import Message
import json
import os

# Load clone data (from your existing code)
CLONE_DATA_FILE = "clone_data.json"

# Helper function to load clone data
def load_clone_data():
    if os.path.exists(CLONE_DATA_FILE):
        with open(CLONE_DATA_FILE, "r") as file:
            return json.load(file)
    return {}

# Your restricted_command function (for limiting access)
@Client.on_message(filters.command("ping"))
async def ping(Client: Client, msg: Message):
    user_id = msg.from_user.id
    clone_data = load_clone_data()

    # Check if the user is the owner of any cloned Client
    for token, details in clone_data.items():
        # Check if owner_id exists in the clone data
        if "owner_id" in details:
            if details["owner_id"] == user_id:
                # If the user is the owner, send a ping response
                await msg.reply("🏓 Pong! You are the owner of this bot.")
                return
        else:
            # If owner_id is missing in the clone data, log a warning
            print(f"Warning: 'owner_id' missing for bot token {token}")

    # If the user is not the owner, deny access to the ping command
    await msg.reply("You are not the owner of this cloned bot, so you cannot use the ping command!")
