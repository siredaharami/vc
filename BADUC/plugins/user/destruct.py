import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.enums import MessageMediaType

from BADUC import SUDOERS
from BADUC.core.clients import app
from BADUC.core.command import *

# Function to handle saving and forwarding media
async def handle_media(client: app, message: Message, media_type: MessageMediaType):
    try:
        # Handle saving the media
        if media_type == MessageMediaType.PHOTO and message.photo:
            # Download the photo
            downloaded_photo = await message.download()
            print(f"Downloaded photo: {downloaded_photo}")

        elif media_type == MessageMediaType.VIDEO and message.video:
            # Download the video
            downloaded_video = await message.download()
            print(f"Downloaded video: {downloaded_video}")

        elif media_type == MessageMediaType.DOCUMENT and message.document:
            # Download the document
            downloaded_document = await message.download()
            print(f"Downloaded document: {downloaded_document}")

        # Forward the media to Saved Messages
        await message.forward(chat_id="me")
        print(f"{media_type.name.capitalize()} forwarded to Saved Messages.")
    except Exception as e:
        print(f"Error handling {media_type.name}: {e}")


# Function to listen for private messages containing media
@app.on_message(filters.private & (filters.photo | filters.video | filters.document))
async def on_private_media(client: app, message: Message):
    # Check for the type of media and apply the appropriate action
    if message.photo:
        await handle_media(client, message, MessageMediaType.PHOTO)

    elif message.video:
        await handle_media(client, message, MessageMediaType.VIDEO)

    elif message.document:
        await handle_media(client, message, MessageMediaType.DOCUMENT)

# timer 
import os
from pyrogram import Client, filters
from pyrogram.types import Message


# Custom filter for self-destruction messages
def self_destruction_filter(_, __, message: Message):
    # Check if the message has a self-destruction timer (modify this logic as per your requirement)
    return getattr(message, "self_destruct_timer", None) is not None

# Register the custom filter
filters.self_destruction = filters.create(self_destruction_filter)

@app.on_message(filters.self_destruction, group=-6)
async def save_timer_media(client: Client, message: Message):
    try:
        # Debugging logs
        print("Message received for self-destruction:")
        print(message)

        # Check if the message contains media
        if message.media:
            print("Downloading media...")
            file_path = await message.download()
            print(f"Media downloaded to: {file_path}")

            # Send the file to Saved Messages
            await client.send_document("me", document=file_path, caption=message.caption or "Saved timer media")
            print("Media sent to Saved Messages.")

            # Remove the temporary file
            os.remove(file_path)
            print(f"File deleted: {file_path}")
        else:
            print("No media found in the message.")
    except Exception as e:
        print(f"Error: {e}")
        
