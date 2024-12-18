import asyncio
import random
from typing import Union

from pyrogram import filters
from yt_dlp import YoutubeDL
from BADUC import SUDOERS
from BADUC.core.clients import app
from BADUC.core.command import *
import cookies

class YouTubeAuthDownloader:
    def __init__(self):
        self.base_url = "https://www.youtube.com/watch?v="

    def get_ytdl_options(self, ytdl_opts, auth_token: str) -> Union[str, dict, list]:
        if isinstance(ytdl_opts, list):
            ytdl_opts += ["--username", "oauth2", "--password", auth_token]
        elif isinstance(ytdl_opts, str):
            ytdl_opts += f"--username oauth2 --password {auth_token} "
        elif isinstance(ytdl_opts, dict):
            ytdl_opts.update({"username": "oauth2", "password": auth_token})
        return ytdl_opts

    async def download(self, link: str, auth_token: str, video: bool = True) -> str:
        loop = asyncio.get_running_loop()

        def download_content():
            ydl_opts = {
                "format": (
                    "(bestvideo[height<=?720][width<=?1280][ext=mp4])+(bestaudio[ext=m4a])"
                    if video
                    else "bestaudio/best"
                ),
                "outtmpl": "downloads/%(id)s.%(ext)s",
                "geo_bypass": True,
                "nocheckcertificate": True,
                "quiet": True,
                "no_warnings": True,
            }
            ydl_opts = self.get_ytdl_options(ydl_opts, auth_token)

            ydl = YoutubeDL(ydl_opts)
            info = ydl.extract_info(link, download=False)
            file_path = os.path.join("downloads", f"{info['id']}.{info['ext']}")
            if not os.path.exists(file_path):
                ydl.download([link])
            return file_path

        file_path = await loop.run_in_executor(None, download_content)
        return file_path
        
def get_random_cookie():
    if not cookies:
        raise FileNotFoundError("No cookies available in the cookies.py file.")
    return random.choice(cookies)


async def check_cookies(video_url):
    cookie = get_random_cookie()
    opts = {
        "format": "bestaudio",
        "quiet": True,
        "cookiefile": cookie,
    }
    try:
        with YoutubeDL(opts) as ytdl:
            ytdl.extract_info(video_url, download=False)
        return True
    except:
        return False


@app.on_message(bad(["cookies"]) & (filters.me | filters.user(SUDOERS)))
async def list_formats(client, message):
    status_message = "sᴛᴀᴛᴜs⚣\n\n"
    status_message += "ᴄᴏᴏᴋɪᴇs⚣︎ ᴄʜᴇᴄᴋɪɴɢ ... "
    status_msg = await message.reply_text(status_message)

    cookie_status = await check_cookies("https://www.youtube.com/watch?v=LLF3GMfNEYU")
    status_message = "sᴛᴀᴛᴜs⚣\n\n"
    status_message += f"ᴄᴏᴏᴋɪᴇs⚣︎ {'✅ ᴀʟɪᴠᴇ' if cookie_status else '❌ ᴅᴇᴀᴅ'}"
    await status_msg.edit_text(status_message)

    use_token = await check_auth_token()
    status_message = "sᴛᴀᴛᴜs⚣︎\n\n"
    status_message += f"ᴄᴏᴏᴋɪᴇs⚣︎ {'✅ ᴀʟɪᴠᴇ' if cookie_status else '❌ ᴅᴇᴀᴅ'}\n"
    await status_msg.edit_text(status_message)
