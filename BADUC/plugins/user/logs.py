import subprocess
import requests
from pyrogram import Client, filters

from BADUC import SUDOERS
from BADUC.core.clients import app
from BADUC.core.command import *

# Function to get logs (example: `tail` command for Linux logs)
def fetch_logs():
    try:
        # Example command to fetch logs; customize as needed
        logs = subprocess.check_output(["tail", "-n", "50", "/var/log/syslog"], stderr=subprocess.STDOUT)
        return logs.decode("utf-8")
    except Exception as e:
        return f"Error fetching logs: {str(e)}"

# Function to upload logs to batbin.me
def upload_logs_to_batbin(log_content):
    url = "https://batbin.me/api/v1/paste"
    data = {"content": log_content}
    response = requests.post(url, json=data)
    if response.status_code == 200:
        return f"https://batbin.me/{response.json().get('key')}"
    else:
        return None

# Command to fetch and upload logs
@app.on_message(bad(["logs"]) & (filters.me | filters.user(SUDOERS)))
async def handle_logs(client, message):
    logs = fetch_logs()
    if logs.startswith("Error"):
        await message.reply(logs)  # Send error message if logs couldn't be fetched
        return

    # Upload logs to batbin.me
    paste_url = upload_logs_to_batbin(logs)

    if paste_url:
        await message.reply(f"Logs uploaded successfully: [View Logs]({paste_url})", disable_web_page_preview=True)
    else:
        await message.reply("Failed to upload logs to batbin.me. Please try again later.")
      
