from pyrogram import Client, filters
from gtts import gTTS
from BADUC import SUDOERS
from BADUC.core.clients import app
from BADUC.core.command import *


@app.on_message(bad(["tts"]) & (filters.me | filters.user(SUDOERS)))
def text_to_speech(client, message):
    text = message.text.split(' ', 1)[2]
    tts = gTTS(text=text, lang='pa')
    tts.save('ʙᴀᴅᴜꜱᴇʀʙᴏᴛ ᴀᴜᴅɪᴏ.mp3')
    client.send_audio(message.chat.id, 'ʙᴀᴅᴜꜱᴇʀʙᴏᴛ ᴀᴜᴅɪᴏ.mp3')
  

__NAME__ = "Tᴛs"
__MENU__ = """
`.tts` - **text to speech .**

"""
