import os
import asyncio
from pyrogram import Client, filters
import openai
from BADUC.core.clients import bot

# Retrieve the OpenAI API key from an environment variable
openai.api_key = os.getenv("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")

# Validate that the API key is set
if not openai.api_key:
    raise ValueError("OpenAI API key not found in environment variables.")

# Function to get response from GPT-4
async def get_gpt4_response(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=150
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"An error occurred: {str(e)}"

# Handler for messages
@bot.on_message(filters.text)
async def gpt4_response_handler(client, message):
    query = message.text
    response = await get_gpt4_response(query)
    await message.reply_text(response)
