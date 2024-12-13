import asyncio
from math import ceil
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton
from typing import Union, List

from BADUC.core.clients import app

class EqInlineKeyboardButton(InlineKeyboardButton):
    def __eq__(self, other):
        return self.text == other.text

    def __lt__(self, other):
        return self.text < other.text

    def __gt__(self, other):
        return self.text > other.text


def paginate_plugins(page_n, plugin_dict, prefix, chat=None):
    if not chat:
        plugins = sorted(
            [
                EqInlineKeyboardButton(
                    x.__NAME__,
                    callback_data="{}_plugin({})".format(
                        prefix, x.__NAME__.lower()
                    ),
                )
                for x in plugin_dict.values()
            ]
        )
    else:
        plugins = sorted(
            [
                EqInlineKeyboardButton(
                    x.__NAME__,
                    callback_data="{}_plugin({},{})".format(
                        prefix, chat, x.__NAME__.lower()
                    ),
                )
                for x in plugin_dict.values()
            ]
        )

    # Adjust rows and columns here
    ROW_SIZE = 5  # Number of rows (Nice)
    COLUMN_SIZE = 3  # Buttons in one row

    # Create button pairs with ROW_SIZE and COLUMN_SIZE
    pairs = [plugins[i:i + COLUMN_SIZE] for i in range(0, len(plugins), COLUMN_SIZE)]
    pages = [pairs[i:i + ROW_SIZE] for i in range(0, len(pairs), ROW_SIZE)]

    max_num_pages = len(pages)
    modulo_page = page_n % max_num_pages

    # Add navigation buttons (if necessary)
    navigation_buttons = [
        EqInlineKeyboardButton(
            "❮",
            callback_data="{}_prev({})".format(prefix, modulo_page),
        ),
        EqInlineKeyboardButton(
            " Oᴡɴᴇʀ ",
            url=f"tg://openmessage?user_id={app.me.id}",
        ),
        EqInlineKeyboardButton(
            "❯",
            callback_data="{}_next({})".format(prefix, modulo_page),
        ),
    ]

    # Current page content
    current_page = pages[modulo_page]

    # Flatten and append navigation buttons
    final_buttons = [row for row in current_page] + [navigation_buttons]

    return final_buttons
