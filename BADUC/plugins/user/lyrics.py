import asyncio
import os
from pyrogram import filters, Client
from pyrogram.types import Message
from BADUC import SUDOERS
from BADUC.core.clients import app
from BADUC.core.command import *

import requests

async def fetch_lyrics(song_name: str) -> str:
    """
    Fetch lyrics from a lyrics API.
    Replace this with a real API request for fetching lyrics.
    """
    api_url = f"https://api.lyrics.ovh/v1/{song_name}"
    try:
        response = requests.get(api_url)
        data = response.json()
        return data.get("lyrics", "No lyrics found.")
    except Exception as e:
        return f"Error fetching lyrics: {str(e)}"

@app.on_message(bad(["lyrics"]) & (filters.me | filters.user(SUDOERS)))
async def send_lyrics(bot: Client, message: Message):
    try:
        cmd = message.command
        song_name = ""

        # Extract the song name from the command or the reply
        if len(cmd) > 1:
            song_name = " ".join(cmd[1:])
        elif message.reply_to_message:
            if message.reply_to_message.audio:
                song_name = f"{message.reply_to_message.audio.title} {message.reply_to_message.audio.performer}"
            elif message.reply_to_message.text:
                song_name = message.reply_to_message.text
        elif not message.reply_to_message and len(cmd) == 1:
            await message.edit("Please provide a song name.")
            await asyncio.sleep(2)
            await message.delete()
            return

        await message.edit(f"Searching lyrics for `{song_name}`...")

        # Assume here we fetch the lyrics somehow, replacing inline bot result fetching
        # For example, using a hypothetical lyrics API or a local method
        lyrics = await fetch_lyrics(song_name)

        if not lyrics:
            await message.edit("No lyrics found for the song.")
            await asyncio.sleep(2)
            await message.delete()
            return

        # Create a text file and save the lyrics
        file_path = f"lyrics_{song_name}.txt"
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(f"Lyrics for: {song_name}\n\n")  # Optional: song name at the top
            file.write(lyrics)  # Write the entire lyrics

        # Send the text file to the user
        await message.reply_document(file_path)

        # Clean up the created file after sending it
        os.remove(file_path)

        await message.delete()

    except Exception as e:
        await message.edit(f"`Failed to find lyrics: {str(e)}`")
        await asyncio.sleep(2)
        await message.delete()


async def fetch_lyrics(song_name: str) -> str:
    """
    Fetch lyrics for the given song name.
    This function should be replaced with a valid method to fetch lyrics.
    For now, it will return a placeholder text for demonstration purposes.
    """
    # This is a placeholder. Replace it with actual lyrics fetching logic
    # Example of lyrics that would be fetched for a song
    return f"Lyrics for {song_name}:\n\nVerse 1:\nLa la la...\nChorus:\nFa la la...\nVerse 2:\nRa ra ra..."
