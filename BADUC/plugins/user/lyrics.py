from pyrogram import Client, filters
import lyricsgenius

from BADUC import SUDOERS
from BADUC.core.clients import app
from BADUC.core.command import *

# Initialize Genius API client
genius = lyricsgenius.Genius("cEY025D7DKhqHyrQsin7ALo0Qq2AAVeuZMqVXlaMwb001UV0vbQ90gUnGktLkjKm")
# Command to get lyrics
@app.on_message(bad(["lyrics"]) & (filters.me | filters.user(SUDOERS)))
async def get_lyrics(client, message):
    if len(message.command) < 2:
        await message.reply("Please provide the song name after the command!")
        return
    
    song_name = " ".join(message.command[1:])
    
    try:
    song = genius.search_song(song_name)
    if song:
        lyrics = song.lyrics
        chunk_size = 4000
        for i in range(0, len(lyrics), chunk_size):
            await message.reply(lyrics[i:i + chunk_size])
    else:
        await message.reply(f"Sorry, I couldn't find the lyrics for '{song_name}'!")
        except Exception as e:
        await message.reply(f"An error occurred while fetching lyrics: {e}")
        print(f"Error: {e}")
