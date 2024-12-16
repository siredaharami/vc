import random
import asyncio

from BADUC import SUDOERS
from BADUC.core.clients import app
from BADUC.core.command import *

from pyrogram import Client, filters
from pyrogram.enums import MessageEntityType as MET, ChatAction as CA
from pyrogram.types import Message
