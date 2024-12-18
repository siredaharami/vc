import os
import sys
import platform
from pyrogram import __version__ as pyrogram_version
from pytgcalls import __version__ as pytgcalls_version
from pyrogram import Client
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from motor.motor_asyncio import AsyncIOMotorClient
from BADUC.core.config import API_ID, API_HASH, STRING_SESSION, MONGO_DB_URL, LOG_GROUP_ID, SUDOERS, BOT_TOKEN
from .logger import LOGGER

BOT_VERSION = "1.0.0"  # Define your bot version here
BOTFATHER_USERNAME = "@BotFather"  # BotFather username


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
        await app.send_message(botfather_chat.id, "/setinline")
        await app.send_message(botfather_chat.id, f"@{bot_username}")
        await app.send_message(botfather_chat.id, "Enabled")
        LOGGER.info("Inline Mode Enabled Successfully.")
    except Exception as e:
        LOGGER.error(f"Failed To Enable Inline Mode: {e}")


async def run_async_clients():
    try:
        LOGGER.info("Starting Userbot...")
        await app.start()
        LOGGER.info("Userbot Started.")
    except Exception as e:
        LOGGER.error(f"Failed To Start Userbot: {e}")
        return

    try:
        python_version = platform.python_version()
        await app.send_message(
            LOG_GROUP_ID,
            f"**Bot Startup Log**\n\n"
            f"**Userbot Started** ✅\n"
            f"**Pyrogram Version:** `{pyrogram_version}`\n"
            f"**PyTgCalls Version:** `{pytgcalls_version}`\n"
            f"**Python Version:** `{python_version}`\n"
            f"**Bot Version:** `{BOT_VERSION}`",
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("Support", url="https://t.me/MASTIWITHFRIENDSXD")]]
            )
        )
        LOGGER.info("Logger Group Message Sent.")
    except Exception as e:
        LOGGER.error(f"Failed To Send Logger Group Message: {e}")

    try:
        await enable_inline_mode()
    except Exception as e:
        LOGGER.error(f"Failed To Enable Inline Mode: {e}")

    try:
        await bot.start()
        LOGGER.info("Helper Bot Started.")
        await bot.send_photo(
            LOG_GROUP_ID,
            photo="https://files.catbox.moe/83d5lc.jpg",
            caption="**Shukla Robot is Alive.**",
            reply_markup=InlineKeyboardMarkup(
                [
                    [InlineKeyboardButton("Support", url="https://t.me/MASTIWITHFRIENDSXD"),
                     InlineKeyboardButton("Update", url="https://t.me/MASTIWITHFRIENDSXD")]
                ]
            )
        )
    except Exception as e:
        LOGGER.error(f"Failed To Start Helper Bot Or Send Message: {e}")

    try:
        LOGGER.info("Starting PyTgCalls...")
        await call.start()
        LOGGER.info("PyTgCalls Started.")
    except Exception as e:
        LOGGER.error(f"Failed To Start PyTgCalls: {e}")

    await sudo_users()
