from typing import Union, List, Pattern
from pyrogram import Client, filters as pyrofl
from pytgcalls import PyTgCalls, filters as pytgfl


# Command filters for bot and app
def cdx(commands: Union[str, List[str]]):
    """Filter commands starting with /, !, or ."""
    return pyrofl.command(commands, prefixes=["/", "!", "."])


def cdz(commands: Union[str, List[str]]):
    """Filter commands starting with no prefix or /, !, ."""
    return pyrofl.command(commands, prefixes=["", "/", "!", "."])


def rgx(pattern: Union[str, Pattern]):
    """Filter messages matching a regex pattern."""
    return pyrofl.regex(pattern)
