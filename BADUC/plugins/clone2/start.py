import random
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton



# List of photos to send randomly
photos = [
    "https://files.catbox.moe/hc6yzu.jpg",
    "https://files.catbox.moe/ww4vzy.jpg",
    "https://files.catbox.moe/3f12ey.jpg",
]

@Client.on_message(filters.command("start"))
async def start(client, message):
    # Select a random photo
    random_photo = random.choice(photos)
    
    # Define the buttons
    buttons = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("⚜️ ᴏꜰꜰɪᴄɪᴀʟ ʙᴏᴛ", url="https://t.me/Baduc2_Bot"),
            ],
            
            [
                InlineKeyboardButton("🔄 ꜱᴜᴘᴘᴏʀᴛ", url="https://t.me/PBX_CHAT"),
                InlineKeyboardButton("🛠 ᴜᴘᴅᴀᴛᴇ", url="https://t.me/HEROKUBIN_01"),
            ]
        ]
    )
    
    # Define the start message
    start_message = (
        "💫 ᴡᴇʟᴄᴏᴍᴇ ᴛᴏ ᴛʜᴇ ʙᴏᴛ ❤️\n"
        "🤖ɪ ᴀᴍ ᴄʟᴏɴᴇ ʙᴏᴛ ꜰᴏʀ ʙᴀᴅᴜꜱᴇʀʙᴏᴛ 🥀\n\n"
        "🔍 ᴍᴏʀᴇ ʜᴇʟᴘ ᴄʟɪᴄᴋ ꜱᴜᴘᴘᴏʀᴛ, ᴏꜰꜰᴄɪᴀʟ ʙᴏᴛ 📂\n"
    )
    
    # Send the photo with the message and buttons
    await client.send_photo(
        chat_id=message.chat.id,
        photo=random_photo,
        caption=start_message,
        reply_markup=buttons
    )
  
