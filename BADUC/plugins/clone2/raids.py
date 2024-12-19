from random import choice
from pyrogram import filters, Client
from pyrogram.types import Message
import asyncio
import random
import time

from BADUC.plugins.bot.clone3 import get_bot_owner
from BADUC.core.command import *
from BADUC.database.data import *

ACTIVATE_RLIST = []

async def is_authorized(client: Client, message: Message):
    bot_id = client.me.id  # The bot's own ID
    user_id = message.from_user.id  # The user ID who sent the message
    owner_id = await get_bot_owner(bot_id)  # Fetch the bot owner's ID
    if owner_id != user_id:  # Check if the user is the bot owner
        await message.reply_text("❌ You're not authorized to use this bot.")
        return False
    return True

# Example of integrating this check into the "praid" function
@Client.on_message(["praid"])
async def raid(Client: Client, m: Message):  
    if not await is_authorized(Client, m):  # Check if the user is authorized
        return

    Bad = "".join(m.text.split(maxsplit=1)[1:]).split(" ", 2)
    if len(Bad) == 2:
        counts = int(Bad[0])
        username = Bad[1]
        if not counts:
            await m.reply_text(f"PBIRAID LIMIT NOT FOUND PLEASE GIVE COUNT!")
            return       
        if not username:
            await m.reply_text("you need to specify an user! Reply to any user or give id/username")
            return
        try:
           user = await Client.get_users(Bad[1])
        except:
           await m.reply_text("**Error:** User not found or may be deleted!")
           return
    elif m.reply_to_message:
        counts = int(Bad[0])
        try:
           user = await Client.get_users(m.reply_to_message.from_user.id)
        except:
           user = m.reply_to_message.from_user 
    else:
        await m.reply_text("Usage: .pbiraid count username or reply")
        return
    if int(m.chat.id) in GROUP:
        await m.reply_text("**Sorry !! i Can't Spam Here.**")
        return
    if int(user.id) in VERIFIED_USERS:
        await m.reply_text("I can't Pbiraid on my developer")
        return
    if int(user.id) in SUDO_USER:
        await m.reply_text("This guy is a sudo users.")
        return
    mention = user.mention
    for _ in range(counts): 
        r = f"{mention} {choice(PBIRAID)}"
        await Client.send_message(m.chat.id, r)
        await asyncio.sleep(0.3)
