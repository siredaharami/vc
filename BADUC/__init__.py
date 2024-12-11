import os
from platform import python_version

import heroku3
from pyrogram import __version__ as pyrogram_version

__version__ = {
    "Pbxbot": "3.0",
    "pyrogram": pyrogram_version,
    "python": python_version(),
}

spam_chats = []
SUDO_USER = SUDO_USERS
OWNER_USERNAME = OWNER_USERNAME
SUDO_USERS.append(OWNER_ID)
