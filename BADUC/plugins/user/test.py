import os
import yt_dlp
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pytgcalls import PyTgCalls
from pytgcalls.exceptions import NoActiveGroupCall
from pytgcalls.types import ChatUpdate, Update, GroupCallConfig
from pytgcalls.types import Call, MediaStream, AudioQuality
from BADUC.core.clients import *

COOKIES_FILE = "cookies.txt"  # Path to your YouTube cookies file


# Ensure download directory exists
DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

@app.on_message(filters.command("play") & filters.private)
async def play_song(client, message):
    if len(message.command) < 2:
        await message.reply("Usage: /play <YouTube URL>", reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("Help", url="https://example.com/help")]]
        ))
        return

    youtube_url = message.command[1]
    await message.reply("Downloading audio... Please wait.")

    try:
        ydl_opts = {
            "format": "bestaudio/best",
            "outtmpl": f"{DOWNLOAD_DIR}/%(title)s.%(ext)s",
            "cookies": COOKIES_FILE,
            "postprocessors": [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'm4a',
            }],
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(youtube_url, download=True)
            filename = ydl.prepare_filename(info).replace(".webm", ".m4a")

        await message.reply(f"Downloaded: {info['title']}\nPlaying in voice chat...")

        # Play audio in voice chat
        await call_client.join_group_call(
            message.chat.id,
            MediaStream(
                file=filename,
                audio_quality=AudioQuality.MEDIUM,  # Adjust as necessary
            )
        )
    except Exception as e:
        await message.reply(f"Error: {str(e)}")

@app.on_message(filters.command("stop") & filters.private)
async def stop_song(client, message):
    try:
        await call_client.leave_group_call(message.chat.id)
        await message.reply("Stopped playing and left the voice chat.")
    except NoActiveGroupCall:
        await message.reply("Error: No active group call.")
    except Exception as e:
        await message.reply(f"Error: {str(e)}")
      
