from pyrogram import Client, filters
from pyrogram.types import ChatMemberUpdated

from BADUC import SUDOERS
from BADUC.core.clients import app
from BADUC.core.command import *

@app.on_chat_member_updated(filters.group)
def welcome_new_user(client, member_update: ChatMemberUpdated):
    if member_update.new_chat_member and member_update.new_chat_member.status == "member":
        user_id = member_update.new_chat_member.user.id
        first_name = member_update.new_chat_member.user.first_name or "User"
        
        welcome_message = f"🌟 **Welcome to the group, [{first_name}](tg://user?id={user_id})!** 🌟\n\nFeel free to chat and engage here!"
        client.send_message(chat_id=member_update.chat.id, text=welcome_message)
