import os
import time
import logging

from os import getenv
from dotenv import load_dotenv
from logging.handlers import RotatingFileHandler


# config variables
if os.path.exists("vars.env"):
    load_dotenv("vars.env")
    
API_ID = int(getenv("API_ID", 0))
API_HASH = getenv("API_HASH", None)
BOT_TOKEN = getenv("BOT_TOKEN", None)
STRING_SESSION = getenv("STRING_SESSION", None)
MONGO_DB_URL = getenv("MONGO_DB_URL", None)
OWNER_ID = int(getenv("OWNER_ID", 0))
LOG_GROUP_ID = int(getenv("LOG_GROUP_ID", 0))
PLAY_IMAGE_URL = getenv("START_IMAGE_URL", "https://files.catbox.moe/6v7esb.jpg")
SUDO_USERS = list(map(int, getenv("SUDO_USERS", "7009601543").split()))
PM_GUARD = bool(getenv("PM_GUARD", True))
PM_GUARD_TEXT = getenv("PM_GUARD_TEXT", "**👋🏻𝐇ყ !**\n❤️𝐎ɯɳҽɾ 𝐈ʂ 𝐎ϝϝℓιɳҽ 𝐒ꪮ 𝐏ℓꫀαʂꫀ 𝐃σɳ'ƚ 𝐒ραɱ🌪️ \n⚡𝐈ϝ 𝐘συ 𝐒ραɱ , 𝐘συ 𝐖ιℓℓ 𝐁ҽ 𝐁ℓσ¢ƙҽԃ 𝐀υƚσɱαƚι¢ℓℓу 🌸 🦋 𝐖αιт 𝐅σя  𝐌у 𝐂υтє [𝐎ωиєя](tg://settings) ❤️**\n**💫 𝐉ᴏɪɴ 𝐎ᴜʀ 𝐓ᴇᴀᴍ 𝐓ʜᴀɴᴋᴜ ❣️")
PM_GUARD_LIMIT = int(getenv("PM_GUARD_LIMIT", 3))
PM_PIC = getenv("PM_PIC", "https://files.catbox.moe/rix20t.jpg")
BOT_PICTURE_URL = "https://files.catbox.moe/83d5lc.jpg"  # Replace with actual URL

# Don't Edit This Codes From This Line

LOGGER = logging.getLogger("main")
runtime = time.time()

FLOODXD = {}
OLD_MSG = {}
PM_LIMIT = {}
PLUGINS = {}
SUDOERS = []

