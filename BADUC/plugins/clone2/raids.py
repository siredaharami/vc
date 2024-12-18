from random import choice
from pyrogram import filters, Client
from pyrogram.types import Message
import asyncio
import random
import time
import os
import json

# import 
from BADUC import SUDOERS as SUDO_USER
from BADUC.database.data import *

from pyrogram import Client, filters
from pyrogram.types import Message
import json
import os

# Load clone data
CLONE_DATA_FILE = "clone_data.json"

def load_clone_data():
    if os.path.exists(CLONE_DATA_FILE):
        with open(CLONE_DATA_FILE, "r") as file:
            return json.load(file)
    return {}

def is_cloned_user(user_id):
    """Check if the user is a cloned bot owner."""
    clone_data = load_clone_data()
    for _, details in clone_data.items():
        if details.get("owner_id") == user_id:
            return True
    return False
    
    
ACTIVATE_RLIST = []


# Decorator for commands restricted to cloned bot owners
def cloned_user_only(func):
    async def wrapper(client: Client, message: Message):
        user_id = message.from_user.id
        if not is_cloned_user(user_id):
            await message.reply("You are not authorized to use this command!")
            return
        return await func(client, message)
    return wrapper
    

@Client.on_message(filters.command("dmraid"))
@cloned_user_only
async def draid(Client: Client, m: Message):  
      Bad = "".join(m.text.split(maxsplit=1)[1:]).split(" ", 2)
      if len(Bad) == 2:
        counts = int(Bad[0])
        username = Bad[1]
        if not counts:
          await m.reply_text(f"RAID LIMIT NOT FOUND PLEASE GIVE COUNT!")
          return       
        if not username:
          await m.reply_text("you need to specify an user! Reply to any user or gime id/username")
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
        await m.reply_text("Usage: .dmraid count username or reply")
        return
      if int(user.id) in VERIFIED_USERS:
         await m.reply_text("I can't raid on my developer")
         return
      if int(user.id) in SUDO_USER:
         await m.reply_text("This guy is a sudo users.")
         return
      mention = user.mention
      await m.reply_text("Dm Raid started..")
      for _ in range(counts): 
         r = f"{choice(RAID)}"
         await Client.send_message(user.id, r)
         await asyncio.sleep(0.3)
          

#porn
@Client.on_message(filters.command("pornraid"))
@cloned_user_only
async def prns(client: Client, message: Message):
    r = await message.reply_text("`ʀᴜᴋᴏ ʙʙʏs🤤🫧`")
    quantity = message.command[1]
    failed = 0
    quantity = int(quantity)
    await r.delete()
    if int(message.chat.id) in GROUP:
        await message.reply_text("`ʏᴏᴜ ᴄᴀɴɴᴏᴛ ᴘᴏʀɴꜱᴘᴀᴍ ɪɴ ᴅᴇᴠᴇʟᴏᴘᴇʀ ᴄʜᴀᴛꜱ!`")
        return
    for _ in range(quantity):
        try:
            file = random.choice(PORM)            
            await client.send_video(chat_id=message.chat.id, video=file)
        except FloodWait as e:
            await asyncio.sleep(e.x)


#eomji

@Client.on_message(filters.command("emojiraid"))
@cloned_user_only
async def emoji(x: Client, e: Message):
      PBX = "".join(e.text.split(maxsplit=1)[1:]).split(" ", 2)

      if len(PBX) == 2:
          ok = await x.get_users(PBX[1])
          counts = int(PBX[0])
          for _ in range(counts):
                reply = choice(EMOJI)
                msg = f"[{ok.first_name}](tg://user?id={ok.id}) {reply}"
                await x.send_message(e.chat.id, msg)
                await asyncio.sleep(0.1)

      elif e.reply_to_message:
          user_id = e.reply_to_message.from_user.id
          ok = await x.get_users(user_id)
          counts = int(PBX[0])
          for _ in range(counts):
                reply = choice(EMOJI)
                msg = f"[{ok.first_name}](tg://user?id={ok.id}) {reply}"
                await x.send_message(e.chat.id, msg)
                await asyncio.sleep(0.1)

      else:
            await e.reply_text(".emojii 10 <ʀᴇᴘʟʏ ᴛᴏ ᴜꜱᴇʀ ᴏʀ ᴜꜱᴇʀɴᴀᴍᴇ>")
            


# DM RAID


@Client.on_message(filters.command("praid"))
@cloned_user_only
async def raid(Client: Client, m: Message):  
      Bad = "".join(m.text.split(maxsplit=1)[1:]).split(" ", 2)
      if len(Bad) == 2:
        counts = int(Bad[0])
        username = Bad[1]
        if not counts:
          await m.reply_text(f"PBIRAID LIMIT NOT FOUND PLEASE GIVE COUNT!")
          return       
        if not username:
          await m.reply_text("you need to specify an user! Reply to any user or gime id/username")
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


#oneword


@Client.on_message(filters.command("oraid"))
@cloned_user_only
async def raid(Client: Client, m: Message):  
      Bad = "".join(m.text.split(maxsplit=1)[1:]).split(" ", 2)
      if len(Bad) == 2:
        counts = int(Bad[0])
        username = Bad[1]
        if not counts:
          await m.reply_text(f"ONEWORDRAID LIMIT NOT FOUND PLEASE GIVE COUNT!")
          return       
        if not username:
          await m.reply_text("you need to specify an user! Reply to any user or gime id/username")
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
         await m.reply_text("**Sorry !! i Can't Spam Here.**")
         return
      if int(user.id) in VERIFIED_USERS:
         await m.reply_text("I can't oneraid on my developer")
         return
      if int(user.id) in SUDO_USER:
         await m.reply_text("This guy is a sudo users.")
         return
      mention = user.mention
      for _ in range(counts): 
         r = f"{mention} {choice(OneWord)}"
         await Client.send_message(m.chat.id, r)
         await asyncio.sleep(0.3)

#HIRAID

@Client.on_message(filters.command("hraid"))
@cloned_user_only
async def raid(Client: Client, m: Message):  
      Bad = "".join(m.text.split(maxsplit=1)[1:]).split(" ", 2)
      if len(Bad) == 2:
        counts = int(Bad[0])
        username = Bad[1]
        if not counts:
          await m.reply_text(f"HIRAID LIMIT NOT FOUND PLEASE GIVE COUNT!")
          return       
        if not username:
          await m.reply_text("you need to specify an user! Reply to any user or gime id/username")
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
         await m.reply_text("**Sorry !! i Can't Spam Here.**")
         return
      if int(user.id) in VERIFIED_USERS:
         await m.reply_text("I can't hiraid on my developer")
         return
      if int(user.id) in SUDO_USER:
         await m.reply_text("This guy is a sudo users.")
         return
      mention = user.mention
      for _ in range(counts): 
         r = f"{mention} {choice(HIRAID)}"
         await Client.send_message(m.chat.id, r)
         await asyncio.sleep(0.3)


@Client.on_message(filters.command("hraid"))
@cloned_user_only
async def raid(Client: Client, m: Message):  
    Bad = "".join(m.text.split(maxsplit=1)[1:]).split(" ", 2)
    if len(Bad) == 2:
        counts = int(Bad[0])
        username = Bad[1]
        if not counts:
            await m.reply_text(f"RAID LIMIT NOT FOUND PLEASE GIVE COUNT!")
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
        await m.reply_text("Usage: .raid count username or reply")
        return

    if int(m.chat.id) in GROUP:
        await m.reply_text("**Sorry !! I can't Spam Here.**")
        return
    if int(user.id) in VERIFIED_USERS:
        await m.reply_text("I can't raid on my developer")
        return
    if int(user.id) in SUDO_USER:
        await m.reply_text("This guy is a sudo user.")
        return
    
    mention = user.mention
    for _ in range(counts): 
        r = f"{mention} {choice(RAID)}"
        await Client.send_message(m.chat.id, r)
        await asyncio.sleep(0.3)
        
