from pyrogram import Client, filters

from BADUC import SUDOERS
from BADUC.core.clients import app
from BADUC.core.command import *

@app.on_message(bad(["repo"]) & (filters.me | filters.user(SUDOERS)))
async def send_repo(client, message):
    repo_link = "https://github.com/Badhacker98/BAD_USERBOT/fork"  # Link to your repo
    group_link = "https://t.me/PBX_CHAT"  # Link to your group (this will be hidden)
    
    # Creating a hidden link using Markdown
    hidden_group_link = f"[Join our group](https://t.me/PBX_CHAT)"
    
    # Sending the response with the repo link and the hidden group link
    await message.reply(f"Here is the repository link: {repo_link}\n\n{hidden_group_link}")
  
