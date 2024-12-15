import os
import sys
from re import sub
from time import time
import asyncio

from pyrogram import Client, filters, enums
from pyrogram.errors import ChatAdminRequired
from pyrogram.types import ChatPermissions, ChatPrivileges, Message


DEVS = ["7009601543"]
admins_in_chat = {}

from BADUC import SUDOERS
from BADUC.core.clients import app
from BADUC.core.command import *

from BADUC.database.misc import extract_user


@app.on_message(bad(["setgcpic"]) & (filters.me | filters.user(SUDOERS)))
async def set_chat_photo(client: Client, message: Message):
    zuzu = (await client.get_chat_member(message.chat.id, client.me.id)).privileges
    can_change_admin = zuzu.can_change_info
    can_change_member = message.chat.permissions.can_change_info
    if not (can_change_admin or can_change_member):
        await message.edit_text("You don't have enough permission")
    if message.reply_to_message:
        if message.reply_to_message.photo:
            await client.set_chat_photo(
                message.chat.id, photo=message.reply_to_message.photo.file_id
            )
            return
    else:
        await message.edit_text("Reply to a photo to set it !")

# Command to change group name
@app.on_message(bad(["setgcname"]) & (filters.me | filters.user(SUDOERS)))
async def set_group_name(client, message):
    if len(message.command) < 2:
        await message.reply_text("Usage: /setname New Group Name")
        return
    
    new_name = " ".join(message.command[1:])
    try:
        await client.set_chat_title(chat_id=message.chat.id, title=new_name)
        await message.reply_text(f"Group name changed to: {new_name}")
    except Exception as e:
        await message.reply_text(f"Error: {e}")

# Command to change group bio (description)
@app.on_message(bad(["setgcbio"]) & (filters.me | filters.user(SUDOERS)))
async def set_group_bio(client, message):
    if len(message.command) < 2:
        await message.reply_text("Usage: /setbio New Group Bio")
        return
    
    new_bio = " ".join(message.command[1:])
    try:
        await client.set_chat_description(chat_id=message.chat.id, description=new_bio)
        await message.reply_text("Group bio updated successfully!")
    except Exception as e:
        await message.reply_text(f"Error: {e}")
      
