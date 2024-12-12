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
                    f"✬ {x.__NAME__} ✬",
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
                    f"✬ {x.__NAME__} ✬",
                    callback_data="{}_plugin({},{})".format(
                        prefix, chat, x.__NAME__.lower()
                    ),
                )
                for x in plugin_dict.values()
            ]
        )

    # Adjust rows and columns here
    ROW_SIZE
