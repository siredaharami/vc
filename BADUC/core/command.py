from typing import Union, List, Pattern
from pyrogram import Client, filters as pyrofl
from pytgcalls import PyTgCalls, filters as pytgfl


# Command filters for bot and app
def bad(commands: Union[str, List[str]]):
    """Filter commands starting with /, !, or ."""
    return pyrofl.command(commands, prefixes=["/", "!", "."])


def sukh(commands: Union[str, List[str]]):
    """Filter commands starting with no prefix or /, !, ."""
    return pyrofl.command(commands, prefixes=["", "/", "!", "."])


def abhi(pattern: Union[str, Pattern]):
    """Filter messages matching a regex pattern."""
    return pyrofl.regex(pattern)

from BADUC.functions.text import (
    super_user_only, sudo_user
)
super_user_only = super_user_only
sudo_user = sudo_user
