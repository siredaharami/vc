import os
from platform import python_version

import heroku3
from pyrogram import __version__ as pyrogram_version

__version__ = {
    "Pbxbot": "3.0",
    "pyrogram": pyrogram_version,
    "python": python_version(),
}
