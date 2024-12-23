import os
import asyncio
from pyrogram import Client, filters
import openai
from BADUC.core.clients import bot

# Retrieve the OpenAI API key from an environment variable
openai.api_key = os.getenv("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")


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
