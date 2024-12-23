import os
from BADUC.core.clients import bot
import asyncio
from pyrogram import Client, filters
import openai

# OpenAI API key
openai.api_key = "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"
# Function to get response from GPT-4
async def get_gpt4_response(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=150
    )
    return response['choices'][0]['message']['content'].strip()

# Handler for messages
@bot.on_message(filters.text)
async def gpt4_response(client, message):
    prompt = message.text
    try:
        response = await get_gpt4_response(prompt)
        await message.reply_text(response)
    except Exception as e:
        await message.reply_text(f"An error occurred: {str(e)}")
