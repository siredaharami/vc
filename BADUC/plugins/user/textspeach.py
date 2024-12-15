from pyrogram import Client, filters
from gtts import gTTS
from BADUC import SUDOERS
from BADUC.core.clients import app
from BADUC.core.command import *

@app.on_message(bad(["tts"]) & (filters.me | filters.user(SUDOERS)))
def text_to_speech(client, message):
    # Ensure the message has enough content
    if len(message.text.split(' ', 1)) < 2:
        message.reply_text("Usage: `.tts <text>`\nPlease provide text to convert to speech.")
        return
    
    # Extract text after the command
    text = message.text.split(' ', 1)[1]
    
    try:
        # Generate TTS audio
        tts = gTTS(text=text, lang='pa')
        audio_file = 'BADUSERBOT_audio.mp3'
        tts.save(audio_file)
        
        # Send the audio file
        client.send_audio(message.chat.id, audio_file)
    except Exception as e:
        # Handle errors and provide feedback
        message.reply_text(f"An error occurred: {str(e)}")

__NAME__ = "Tᴛs"
__MENU__ = """
`.tts <text>` - **Convert text to speech.**
"""
