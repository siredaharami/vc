import os
import sys
import platform
from pytgcalls import PyTgCalls
from pyrogram import __version__ as pyrogram_version
from pytgcalls import __version__ as pytgcalls_version
from pyrogram import Client
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from motor.motor_asyncio import AsyncIOMotorClient
from BADUC.core.config import (
    API_ID,
    API_HASH,
    STRING_SESSION,
    MONGO_DB_URL,
    LOG_GROUP_ID,
    SUDOERS,
    BOT_TOKEN,
    BOT_PICTURE_URL,  # Add URL in your config
)
from .logger import LOGGER

BOT_VERSION = "3.0.0"  # Define your bot version here
BOTFATHER_USERNAME = "BotFather"  # BotFather username
BOT_INLINE_PLACEHOLDER = "ʙᴀᴅᴜꜱᴇʀʙᴏᴛ"  # Inline Placeholder
BOT_NAME = "ʙᴀᴅᴜꜱᴇʀʙᴏᴛ ᴀꜱꜱɪꜱᴛᴀɴᴛ"  # Bot Name


def async_config():
    LOGGER.info("Checking Variables...")
    if not API_ID:
        LOGGER.error("'API_ID' - Not Found!")
        sys.exit()
    if not API_HASH:
        LOGGER.error("'API_HASH' - Not Found!")
        sys.exit()
    if not BOT_TOKEN:
        LOGGER.error("'BOT_TOKEN' - Not Found!")
        sys.exit()
    if not STRING_SESSION:
        LOGGER.error("'STRING_SESSION' - Not Found!")
        sys.exit()
    if not MONGO_DB_URL:
        LOGGER.error("'MONGO_DB_URL' - Not Found!")
        sys.exit()
    if not LOG_GROUP_ID:
        LOGGER.error("'LOG_GROUP_ID' - Not Found!")
        sys.exit()
    if not BOT_PICTURE_URL:
        LOGGER.error("'BOT_PICTURE_URL' - Not Found!")
        sys.exit()
    LOGGER.info("All Required Variables Collected.")


def async_dirs():
    LOGGER.info("Initializing Directories...")
    if "downloads" not in os.listdir():
        os.mkdir("downloads")
    if "cache" not in os.listdir():
        os.mkdir("cache")
    
    for file in os.listdir():
        if file.endswith(".session") or file.endswith(".session-journal"):
            os.remove(file)
    LOGGER.info("Directories Initialized.")

async_dirs()

app = Client(
    name="BADUC",
    api_id=API_ID,
    api_hash=API_HASH,
    session_string=STRING_SESSION,
)

bot = Client(
    name="BADUCSUPPORT",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
)

call = PyTgCalls(app)


def mongodbase():
    global mongodb
    try:
        LOGGER.info("Connecting To Your Database...")
        async_client = AsyncIOMotorClient
        mongobase = async_client(MONGO_DB_URL)
        mongodb = mongobase.BADUC
        LOGGER.info("Connected To Your Database.")
    except Exception as e:
        LOGGER.error(f"Failed To Connect To Database: {e}")
        sys.exit()

mongodbase()


async def sudo_users():
    sudoersdb = mongodb.sudoers
    sudoers = await sudoersdb.find_one({"sudo": "sudo"})
    sudoers = [] if not sudoers else sudoers["sudoers"]
    if sudoers:
        for user_id in sudoers:
            SUDOERS.append(int(user_id))
    LOGGER.info("Sudo Users Loaded.")


async def enable_inline_mode():
    LOGGER.info("Enabling Inline Mode via BotFather...")
    try:
        if not app.is_connected:
            LOGGER.info("Starting Userbot Client...")
            await app.start()

        bot_details = await bot.get_me()
        bot_username = bot_details.username

        if not bot_username:
            LOGGER.error("Bot Username Not Found!")
            return

        LOGGER.info(f"Bot Username: @{bot_username}")

        botfather_chat = await app.get_chat(BOTFATHER_USERNAME)
        
        # Set inline mode and placeholder
        await app.send_message(botfather_chat.id, "/setinline")
        await app.send_message(botfather_chat.id, f"@{bot_username}")
        await app.send_message(botfather_chat.id, BOT_INLINE_PLACEHOLDER)
        
        # Set bot name
        await app.send_message(botfather_chat.id, "/setname")
        await app.send_message(botfather_chat.id, f"@{bot_username}")
        await app.send_message(botfather_chat.id, BOT_NAME)

        # Set bot profile picture using URL
        await app.send_message(botfather_chat.id, "/setuserpic")
        await app.send_message(botfather_chat.id, f"@{bot_username}")
        await app.send_photo(botfather_chat.id, BOT_PICTURE_URL)
        
        # Add commands
        await app.send_message(botfather_chat.id, "/setcommands")
        await app.send_message(botfather_chat.id, f"@{bot_username}")
        await app.send_message(
            botfather_chat.id,
            "start - Start the bot\nhelp - Get help information",
        )
        
        LOGGER.info("Inline Mode, Name, Picture, and Commands Set Successfully.")
    except Exception as e:
        LOGGER.error(f"Failed To Enable Inline Mode or Set Bot Details: {e}")


async def run_async_clients():
    try:
        # Start Bot First
        LOGGER.info("Starting Helper Bot...")
        await bot.start()
        LOGGER.info("Helper Bot Started.")
        
        python_version = platform.python_version()
        
        # Send detailed startup message in logger group
        await bot.send_photo(
            LOG_GROUP_ID,
            photo=BOT_PICTURE_URL,  # Use the same bot picture URL here
            caption=(
                f"**Baduser Bot is Alive!** ✅\n\n"
                f"**🔹 Python ➠ ** `{python_version}`\n"
                f"**🔹 Pyrogram ➠ ** `{pyrogram_version}`\n"
                f"**🔹 Pytgcalls ➠ ** `{pytgcalls_version}`\n"
                f"**🔹 Version ➠ ** `{BOT_VERSION}`"
            ),
            reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                "💫 ꜱᴛᴀʀᴛ ᴍᴇ",
                                url=f"https://t.me/{bot.me.username}?start=start",
                            ),
                            InlineKeyboardButton(
                                "💖 ʀᴇᴘᴏ",
                                url="https://github.com/Badhacker98/BAD_USERBOT/fork",
                            ),
                        ],
                        [
                            InlineKeyboardButton(
                                "💬 ꜱᴜᴘᴘᴏʀᴛ", url="https://t.me/PBX_CHAT"
                            ),
                            InlineKeyboardButton(
                                "⚜️ ᴜᴘᴅᴀᴛᴇ",
                                url="https://t.me/HEROKUBIN_01",
                            ),
                        ],
                    ]
                ),
        )
        LOGGER.info("Logger Group Message Sent (Helper Bot).")
    except Exception as e:
        LOGGER.error(f"Failed To Start Helper Bot Or Send Message: {e}")
        return

    try:
        # Start Userbot (Assistant)
        LOGGER.info("Starting Userbot...")
        await app.start()
        LOGGER.info("Userbot Started.")
        
        # Automatically join specified groups
        try:
            LOGGER.info("Joining specified groups...")
            await app.join_chat("PBX_CHAT")
            await app.join_chat("HEROKUBIN_01")
            LOGGER.info("Successfully joined specified groups.")
        except Exception as e:
            LOGGER.error(f"Failed to join groups: {e}")

        # Send simple alive message in logger group
        await app.send_message(
            LOG_GROUP_ID,
            "**ʙᴀᴅᴜꜱᴇʀʙᴏᴛ ꜱᴛᴀʀᴛ ! ** ✅",
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("ꜱᴜᴘᴘᴏʀᴛ", url="https://t.me/PBX_CHAT")]]
            ),
        )
        LOGGER.info("Logger Group Message Sent (Userbot).")
    except Exception as e:
        LOGGER.error(f"Failed To Start Userbot Or Send Message: {e}")
        return

    try:
        LOGGER.info("Starting PyTgCalls...")
        await call.start()
        LOGGER.info("PyTgCalls Started.")
    except Exception as e:
        LOGGER.error(f"Failed To Start PyTgCalls: {e}")

    try:
        await enable_inline_mode()
    except Exception as e:
        LOGGER.error(f"Failed To Enable Inline Mode: {e}")

    await sudo_users()
