import os, sys

from pyrogram import Client
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pytgcalls import PyTgCalls
from motor.motor_asyncio import AsyncIOMotorClient

from BADUC.core.config import API_ID, API_HASH, STRING_SESSION, MONGO_DB_URL, LOG_GROUP_ID, SUDOERS, BOT_TOKEN
from .logger import LOGGER

BOTFATHER_USERNAME = "@BotFather"  # BotFather username

def async_config():
    LOGGER.info("Checking Variables ...")
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
        if file.endswith(".session"):
            os.remove(file)
        if file.endswith(".session-journal"):
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
    """
    Automates enabling Inline Mode in BotFather for the bot.
    """
    LOGGER.info("Enabling Inline Mode via BotFather...")
    try:
        # Ensure the app is started
        if not app.is_connected:
            LOGGER.info("Starting Userbot Client...")
            await app.start()

        # Fetch bot details to get the username
        bot_details = await bot.get_me()
        bot_username = bot_details.username  # Fetch bot username dynamically

        if not bot_username:
            LOGGER.error("Bot Username Not Found!")
            return

        LOGGER.info(f"Bot Username: @{bot_username}")

        # Start conversation with BotFather
        botfather_chat = await app.get_chat(BOTFATHER_USERNAME)
        await app.send_message(botfather_chat.id, "/setinline")
        
        # Select bot username dynamically
        await app.send_message(botfather_chat.id, f"@{bot_username}")
        
        # Enable inline mode (confirmation message)
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
        LOGGER.info("Sending Logger Group Message...")
        await app.send_message(
            LOG_GROUP_ID,
            "**sʜᴜᴋʟᴀ ᴜsᴇʀʙᴏᴛ ɪs ᴀʟɪᴠᴇ**",
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("Support", url="https://t.me/MASTIWITHFRIENDSXD")]]
            )
        )
        LOGGER.info("Logger Group Message Sent.")
    except Exception as e:
        LOGGER.error(f"Failed To Send Message To Logger Group: {e}")

    try:
        await app.join_chat("dn")
        await app.join_chat("bdu")
    except Exception as e:
        LOGGER.error(f"Failed To Join Chats: {e}")

    try:
        await enable_inline_mode()  # Call the function to enable inline mode
    except Exception as e:
        LOGGER.error(f"Failed To Enable Inline Mode: {e}")

    try:
        await bot.start()
        LOGGER.info("Helper Bot Started.")
        await bot.send_message(
            LOG_GROUP_ID,
            "**sʜᴜᴋʟᴀ ʀᴏʙᴏᴛ ɪs ᴀʟɪᴠᴇ.**",
            photo="https://example.com/photo.jpg",  # Add photo URL
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("Help", callback_data="help_menu")],
                 [InlineKeyboardButton("Support", url="https://t.me/MASTIWITHFRIENDSXD")],
                 [InlineKeyboardButton("Update", callback_data="update")]]
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
