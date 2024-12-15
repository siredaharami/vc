import os
from pyrogram import Client, filters
from pyrogram.types import Message
from telegraph import upload_file

from BADUC import SUDOERS
from BADUC.core.clients import bot
from BADUC.core.command import *

# Create a directory for downloads
if not os.path.exists("downloads"):
    os.makedirs("downloads")

@bot.on_message(filters.sticker & filters.private)
async def sticker_to_video(client, message: Message):
    sticker = message.sticker

    if not sticker.is_animated:  # Check if the sticker is a static image
        await message.reply_text("This sticker is not a GIF sticker.")
        return

    # Download the sticker as a video
    file_path = await client.download_media(message, file_name="downloads/")
    video_path = f"{file_path}.mp4"

    # Convert WebM (sticker format) to MP4
    os.system(f"ffmpeg -i {file_path} -c:v libx264 -crf 23 {video_path}")

    # Upload the video to Telegraph and get the link
    try:
        response = upload_file(video_path)
        telegraph_link = f"https://telegra.ph{response[0]['src']}"
        await message.reply_text(f"Here is your video link: [Click here]({telegraph_link})", disable_web_page_preview=True)
    except Exception as e:
        await message.reply_text(f"Failed to upload the video to Telegraph: {e}")

    # Clean up
    os.remove(file_path)
    os.remove(video_path)
  
