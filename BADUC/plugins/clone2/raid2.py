from random import choice
from pyrogram import filters, Client
from pyrogram.types import Message
from BADUC.plugins.bot.clone3 import get_bot_owner
import asyncio
import random
import time

# import 
from BADUC import SUDOERS as SUDO_USER
from BADUC.database.data import *

ACTIVATE_RLIST = []

# Function to check if the user is authorized
async def is_authorized(client, message):
    bot_info = await client.get_me()  # Retrieve current bot's details
    bot_id = bot_info.id  # Get the current bot's ID
    user_id = message.from_user.id  # Get the user's ID

    owner_id = await get_bot_owner(bot_id)  # Assuming get_bot_owner function is available
    if owner_id != user_id:
        await message.reply_text("❌ You're not authorized to use this bot.")
        return False
    return True



# DM RAID
@Client.on_message(filters.command("praid"))
async def raid(Client: Client, m: Message):  
    if not await is_authorized(Client, m):
        return  # If not authorized, exit the function
    
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
        await m.reply_text("**Sorry !! I can't Spam Here.**")
        return
    if int(user.id) in VERIFIED_USERS:
        await m.reply_text("I can't Pbiraid on my developer")
        return
    if int(user.id) in SUDO_USER:
        await m.reply_text("This guy is a sudo user.")
        return
    mention = user.mention
    for _ in range(counts): 
        r = f"{mention} {choice(PBIRAID)}"
        await Client.send_message(m.chat.id, r)
        await asyncio.sleep(0.3)


# OneWord Raid
@Client.on_message(filters.command("oraid"))
async def raid(Client: Client, m: Message):  
    if not await is_authorized(Client, m):
        return  # If not authorized, exit the function
    
    Bad = "".join(m.text.split(maxsplit=1)[1:]).split(" ", 2)
    if len(Bad) == 2:
        counts = int(Bad[0])
        username = Bad[1]
        if not counts:
            await m.reply_text(f"ONEWORDRAID LIMIT NOT FOUND PLEASE GIVE COUNT!")
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
        await m.reply_text("Usage: .oneraid count username or reply")
        return
    if int(m.chat.id) in GROUP:
        await m.reply_text("**Sorry !! I can't Spam Here.**")
        return
    if int(user.id) in VERIFIED_USERS:
        await m.reply_text("I can't oneraid on my developer")
        return
    if int(user.id) in SUDO_USER:
        await m.reply_text("This guy is a sudo user.")
        return
    mention = user.mention
    for _ in range(counts): 
        r = f"{mention} {choice(OneWord)}"
        await Client.send_message(m.chat.id, r)
        await asyncio.sleep(0.3)


# HIRAID
@Client.on_message(filters.command("hraid"))
async def raid(Client: Client, m: Message):  
    if not await is_authorized(Client, m):
        return  # If not authorized, exit the function
    
    Bad = "".join(m.text.split(maxsplit=1)[1:]).split(" ", 2)
    if len(Bad) == 2:
        counts = int(Bad[0])
        username = Bad[1]
        if not counts:
            await m.reply_text(f"HIRAID LIMIT NOT FOUND PLEASE GIVE COUNT!")
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
        await m.reply_text("Usage: .hiraid count username or reply")
        return
    if int(m.chat.id) in GROUP:
        await m.reply_text("**Sorry !! I can't Spam Here.**")
        return
    if int(user.id) in VERIFIED_USERS:
        await m.reply_text("I can't hiraid on my developer")
        return
    if int(user.id) in SUDO_USER:
        await m.reply_text("This guy is a sudo user.")
        return
    mention = user.mention
    for _ in range(counts): 
        r = f"{mention} {choice(HIRAID)}"
        await Client.send_message(m.chat.id, r)
        await asyncio.sleep(0.3)

