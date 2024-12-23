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
