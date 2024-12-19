from random import choice
from pyrogram import filters, Client
from pyrogram.types import Message
import asyncio
import random
from BADUC.plugins.bot.clone3 import get_bot_owner

@Client.on_message(filters.command(["dmraid", "pornraid", "emojiraid", "praid", "oraid", "hraid"]))
async def raid_command(client: Client, message: Message):
    bot_info = await client.get_me()
    bot_id = bot_info.id
    user_id = message.from_user.id
    
    # Authorization check
    owner_id = await get_bot_owner(bot_id)
    if owner_id != user_id:
        await message.reply_text("❌ You're not authorized to use this bot.")
        return

    command = message.command[0]  # Get the command
    args = message.text.split()[1:]  # Split arguments after the command
    counts = int(args[0]) if args else 10  # Default count to 10 if not provided
    username = args[1] if len(args) > 1 else None

    if command == "dmraid":
        await dmraid(client, message, counts, username)
    elif command == "pornraid":
        await pornraid(client, message, counts)
    elif command == "emojiraid":
        await emojiraid(client, message, counts, username)
    elif command == "praid":
        await praid(client, message, counts, username)
    elif command == "oraid":
        await oraid(client, message, counts, username)
    elif command == "hraid":
        await hraid(client, message, counts, username)

# Example: DM Raid Function
async def dmraid(client: Client, message: Message, counts, username):
    try:
        user = await client.get_users(username)
    except Exception as e:
        await message.reply_text(f"Error: {str(e)}")
        return
    
    for _ in range(counts):
        try:
            text = f"Hello {user.mention}, this is a DM raid!"
            await client.send_message(user.id, text)
            await asyncio.sleep(0.5)
        except Exception as e:
            await message.reply_text(f"Error: {str(e)}")
            break

# Example: Porn Raid Function
async def pornraid(client: Client, message: Message, counts):
    for _ in range(counts):
        try:
            video = random.choice(["video1.mp4", "video2.mp4", "video3.mp4"])  # Replace with actual video files
            await client.send_video(message.chat.id, video)
            await asyncio.sleep(0.5)
        except Exception as e:
            await message.reply_text(f"Error: {str(e)}")
            break

# Add similar sub-functions for other raid commands: emojiraid, praid, oraid, hraid
