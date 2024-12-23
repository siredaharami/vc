import time
import requests
from pyrogram import filters
from pyrogram.enums import ChatAction

from BADUC.core.clients import bot

# Helper function to get chat GPT response
def get_chat_gpt_response(question):
    try:
        response = requests.get(f'https://chatgpt.apinepdev.workers.dev/?question={question}')
        response.raise_for_status()
        return response.json().get("answer", "No answer available")
    except (requests.RequestException, ValueError):
        return "Error retrieving response."

@bot.on_message(filters.me)
async def chat_gpt(bot, message):
    question = message.text.strip()

    if not question:
        # Skip processing if the message is empty
        return

    await bot.send_chat_action(message.chat.id, ChatAction.TYPING)

    answer = get_chat_gpt_response(question)

    await message.reply_text(answer)

# Optional: Remove the error handler if you don't need to handle errors explicitly
