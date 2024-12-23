from pyrogram import Client, filters
from gtts import gTTS
from BADUC import SUDOERS
from BADUC.core.command import *
import os

@Client.on_message(bad(["tts"]) & (filters.me | filters.user(SUDOERS)))
async def text_to_speech(client, message):
    # Ensure the message has enough content
    if len(message.text.split(' ', 1)) < 2:
        await message.reply_text("Usage: `.tts <text>`\nPlease provide text to convert to speech.")
        await message.delete()
        return
    
    # Extract text after the command
    text = message.text.split(' ', 1)[1]
    
    try:
        # Generate TTS audio
        tts = gTTS(text=text, lang='pa')
        audio_file = 'BADUSERBOT_audio.mp3'
        tts.save(audio_file)
        
        # Send the audio file as a reply to the original message
        if message.reply_to_message:
            await message.reply_to_message.reply_audio(audio_file)
        else:
            await message.reply_audio(audio_file)
        
        # Delete the command message after sending the audio
        await message.delete()
    except Exception as e:
        # Handle errors and provide feedback
        await message.reply_text(f"An error occurred: {str(e)}")
    
    # Clean up the saved audio file
    if os.path.exists(audio_file):
        os.remove(audio_file)

