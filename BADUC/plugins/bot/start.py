from pyrogram import Client, filters
from BADUC.core.clients import bot
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

# Photo URLs for Start Command
start_photos = [
    "https://files.catbox.moe/r4m4n7.jpg",
    "https://files.catbox.moe/8cv5nb.jpg",
    "https://files.catbox.moe/uxqorv.jpg"
]
current_photo = 0  # To track the current photo index

async def get_next_photo():
    global current_photo
    photo = start_photos[current_photo]
    current_photo = (current_photo + 1) % len(start_photos)
    return photo

# Start Command
@bot.on_message(filters.command("start"))
async def start(bot, message):
    # Buttons with text
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("ᴏᴡɴᴇʀ 💫", url="https://t.me/ll_BAD_MUNDA_ll")],
        [InlineKeyboardButton("ꜱᴜᴘᴘᴏʀᴛ 📁", url="https://t.me/PBX_CHAT"),
         InlineKeyboardButton("ᴜᴘᴅᴀᴛᴇ 📂", url="https://t.me/HEROKUBIN_01")],
        [InlineKeyboardButton("ʀᴇᴘᴏ 📌", url="https://github.com/Badhacker98/BAD_USERBOT/fork"),
         InlineKeyboardButton("ʜᴇʟᴘ 💢", callback_data="help")]
    ])
    photo = await get_next_photo()
    caption = (
        f"👋🏻 ʜʏ, {message.from_user.first_name} - ᴡᴀʀʀɪᴏʀꜱ ᴏꜰ ʙᴀᴅᴜꜱᴇʀʙᴏᴛ 👻\n\n"
        "🪄 ɪ ᴀᴍ ʏᴏᴜʀ ᴛʀᴜꜱᴛʏ ᴄᴏᴍᴘᴀɴɪᴏɴ ᴛʜᴇ ʙᴀᴅᴜꜱᴇʀʙᴏᴛ ᴀꜱꜱɪꜱᴛᴀɴᴛ ! 🚀\n\n"
        "👋🏻 ɪ ᴀᴍ ᴀᴅᴠᴀɴᴄᴇᴅ ⛏ ᴀɴᴅ sᴜᴘᴇʀғᴀsᴛ ⛓ ᴛᴇʟᴇɢʀᴀᴍ ᴜsᴇʀʙᴏᴛ 🤖.\n"
        "💫 ᴡᴇʟᴄᴏᴍᴇ ᴛᴏ ʙᴀᴅᴜꜱᴇʀʙᴏᴛ ᴀꜱꜱɪꜱᴛᴀɴᴛ ᴡʜɪʀᴇ ᴘᴏᴡᴇʀ ᴍᴇᴇᴛꜱ ᴇꜰꜰɪᴄɪᴇɴᴄʏ 🤖!\n\n"
        "❤️ @PBX_CHAT ❤️"
    )
    await message.reply_photo(photo, caption=caption, reply_markup=keyboard)

# Callback Query Handler
@bot.on_callback_query()
async def callback_query_handler(bot, query):
    if query.data == "help":
        # Help Menu Buttons
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("ɢᴀᴍᴇ 🎮", callback_data="game"),
             InlineKeyboardButton("ᴄʟᴏɴᴇ 🎰", callback_data="clone")],
            [InlineKeyboardButton("ꜱᴛʀɪɴɢ ꜱᴇꜱꜱɪᴏɴ 🎯", url="https://your-string-session-link.com")]
        ])
        await query.message.edit_text(
            "📖 ʜᴇʟᴘ ᴍᴇɴᴜ\n\n"
            "1️⃣ ɢᴀᴍᴇ: ɪɴꜱᴛʀᴜᴄᴛɪᴏɴꜱ ꜰᴏʀ ᴛʜᴇ ɢᴀᴍᴇ.\n"
            "2️⃣ ᴄʟᴏɴᴇ: ʜᴏᴡ ᴛᴏ ᴜꜱᴇ ᴄʟᴏɴɪɴɢ ꜰᴇᴀᴛᴜʀᴇꜱ.\n"
            "3️⃣ ꜱᴛʀɪɴɢ ꜱᴇꜱꜱɪᴏɴ: ɢᴇɴᴇʀᴀᴛᴇ ᴀ ꜱᴛʀɪɴɢ ꜱᴇꜱꜱɪᴏɴ ᴇᴀꜱɪʟʏ.\n\n"
            "🔘 ᴄʟɪᴄᴋ ᴛʜᴇ ʙᴜᴛᴛᴏɴꜱ ʙᴇʟᴏᴡ ᴛᴏ ᴘʀᴏᴄᴇᴇᴅ.",
            reply_markup=keyboard
        )

    elif query.data == "game":
        # Game Text with Back Button
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("ʙᴀᴄᴋ", callback_data="help")]
        ])
        await query.message.edit_text(
            "🎮 ɢᴀᴍᴇ ᴍᴇɴᴜ \n\n"
            "ᴛʏᴘᴇꜱ /games ꜱʜᴏᴡ ɢᴀᴍᴇꜱ ʙᴜᴛᴛᴏɴ ᴄʟɪᴄᴋ ʙᴜᴛᴛᴏɴ ᴇɴᴊᴏʏ\n\n"
            "👻 ᴄʟɪᴄᴋ 'ʙᴀᴄᴋ' ᴛᴏ ʀᴇᴛᴜʀɴ ᴛᴏ ᴛʜᴇ ʜᴇʟᴘ ᴍᴇɴᴜ.",
            reply_markup=keyboard
        )

    elif query.data == "clone":
        # Clone Buttons
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("🪄 ꜱᴇꜱꜱɪᴏɴ ᴄʟᴏɴᴇ", callback_data="session_clone"),
             InlineKeyboardButton("💫 ʙᴏᴛ ᴄʟᴏɴᴇ", callback_data="bot_clone")],
            [InlineKeyboardButton("⬅️ ʙᴀᴄᴋ", callback_data="help")]
        ])
        await query.message.edit_text(
            "💢 ꜱᴇʟᴇᴄᴛ ᴛʜᴇ ᴄʟᴏɴɪɴɢ ꜰᴇᴀᴛᴜʀᴇ ʏᴏᴜ ᴡᴀɴᴛ ᴛᴏ ᴜꜱᴇ :\n\n"
            "🔘 ꜱᴇꜱꜱɪᴏɴ ᴄʟᴏɴᴇ: ᴄʟᴏɴᴇ ʏᴏᴜʀ ꜱᴇꜱꜱɪᴏɴ ꜱᴛʀɪɴɢ.\n"
            "🔘 ʙᴏᴛ ᴄʟᴏɴᴇ: ᴄʟᴏɴᴇ ᴀ ʙᴏᴛ ᴛᴏᴋᴇɴ.\n\n"
            "👻 ᴄʟɪᴄᴋ 'ʙᴀᴄᴋ' ᴛᴏ ʀᴇᴛᴜʀɴ ᴛᴏ ᴛʜᴇ ʜᴇʟᴘ ᴍᴇɴᴜ.",
            reply_markup=keyboard
        )

    elif query.data == "session_clone":
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("ʙᴀᴄᴋ ᴛᴏ ᴄʟᴏɴᴇ ᴍᴇɴᴜ", callback_data="clone")]
        ])
        await query.message.edit_text(
            "💢 ꜱᴇꜱꜱɪᴏɴ ᴄʟᴏɴᴇ ɪɴꜱᴛʀᴜᴄᴛɪᴏɴꜱ:\n\n"
            "1️⃣ ᴜꜱᴇ /sessionclone [PASTE_SESSION_STRING_HERE]\n"
            "ᴇxᴀᴍᴘʟᴇ: /sessionclone BQGIzloAxVcKLTx6W9kSvRVtHGy..\n\n"
            "💢 ** ᴅᴇʟᴇᴛᴇ ꜱᴇꜱꜱɪᴏɴ ᴄʟᴏɴᴇ **\n\n"
            "2️⃣ ᴜꜱᴇ /sessiondelete [PASTE_SESSION_STRING_HERE]\n"
            "ᴇxᴀᴍᴘʟᴇ: /sessiondelete BQGIzloAxVcKLTx6W9kSvRVtHGy..\n\n"
            "👻 ᴄʟɪᴄᴋ 'ʙᴀᴄᴋ ᴛᴏ ᴄʟᴏɴᴇ ᴍᴇɴᴜ' ᴛᴏ ʀᴇᴛᴜʀɴ.",
            reply_markup=keyboard
        )

    elif query.data == "bot_clone":
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("ʙᴀᴄᴋ ᴛᴏ ᴄʟᴏɴᴇ ᴍᴇɴᴜ", callback_data="clone")]
        ])
        await query.message.edit_text(
            "💢ʙᴏᴛ ᴄʟᴏɴᴇ ɪɴꜱᴛʀᴜᴄᴛɪᴏɴꜱ:\n\n"
            "1️⃣ ᴜꜱᴇ /botclone [PASTE_BOT_TOKEN_HERE]\n"
            "ᴇxᴀᴍᴘʟᴇ: /botclone 7656510911:AAEyXD6baANnUNZ...\n\n"
            "💢 ** ᴅᴇʟᴇᴛᴇ ʙᴏᴛ ᴄʟᴏɴᴇ **\\n"
            "2️⃣ ᴜꜱᴇ /botdelete [PASTE_BOT_TOKEN_HERE]\n"
            "ᴇxᴀᴍᴘʟᴇ: /botdelete 7656510911:AAEyXD6baANnUNZ...\n\n"
            "👻 ᴄʟɪᴄᴋ 'ʙᴀᴄᴋ ᴛᴏ ᴄʟᴏɴᴇ ᴍᴇɴᴜ' ᴛᴏ ʀᴇᴛᴜʀɴ.",
            reply_markup=keyboard
        )
        
