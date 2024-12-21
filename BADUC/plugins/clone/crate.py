from pyrogram import Client, filters
from pyrogram.errors import FloodWait

from BADUC import SUDOERS
from BADUC.core.command import *

# Command to create a group
@Client.on_message(bad(["crategc"]) & (filters.me | filters.user(SUDOERS)))
async def create_group(client, message):
    try:
        # Ensure the group name is passed with the command
        if len(message.text.split()) < 2:
            await message.reply("Please provide a group name after the command. Example: .create_group MyGroup")
            return
        
        group_name = message.text.split(' ', 1)[1]
        
        # Create a group (supergroup in this case)
        group = await client.create_chat(name=group_name, type='supergroup')
        await message.reply(f"Group created successfully: {group.name} (ID: {group.id})")
    except FloodWait as e:
        await message.reply(f"Rate limit exceeded, please wait for {e.x} seconds.")
    except Exception as e:
        await message.reply(f"Error creating group: {e}")

# Command to create a channel
@Client.on_message(bad(["cratech"]) & (filters.me | filters.user(SUDOERS)))
async def create_channel(client, message):
    try:
        # Ensure the channel name is passed with the command
        if len(message.text.split()) < 2:
            await message.reply("Please provide a channel name after the command. Example: .create_channel MyChannel")
            return
        
        channel_name = message.text.split(' ', 1)[1]
        
        # Create a channel
        channel = await client.create_chat(name=channel_name, type='channel')
        await message.reply(f"Channel created successfully: {channel.name} (ID: {channel.id})")
    except FloodWait as e:
        await message.reply(f"Rate limit exceeded, please wait for {e.x} seconds.")
    except Exception as e:
        await message.reply(f"Error creating channel: {e}")

      
