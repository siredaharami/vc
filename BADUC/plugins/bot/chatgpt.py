import os
from BADUC.core.clients import bot
import asyncio
from pyrogram import Client, filters
import openai

# OpenAI API key
openai.api_key = "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"

# Function to get response from GPT-4
async def get_gpt4_response(prompt):
    loop = asyncio.get_event_loop()
    response = await loop.run_in_executor(None, lambda: openai.Completion.create(
        engine="text-davinci-004",
        prompt=prompt,
        max_tokens=150
    ))
    return response.choices[0].text.strip()

# Handler for messages
@bot.on_message(filters.text)
async def gpt4_response(client, message):
    prompt = message.text
    response = await get_gpt4_response(prompt)
    await message.reply_text(response)
