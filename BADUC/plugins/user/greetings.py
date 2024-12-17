from html import escape
from pyrogram import filters
from pyrogram.enums import ChatMemberStatus as CMS
from pyrogram.types import ChatMemberUpdated, Message

from BADUC.core.clients import app
from BADUC.database.greetings.greetings_db import Greetings
from BADUC.database.greetings.parser import escape_invalid_curly_brackets, mention_html

ChatType = enums.ChatType

# Helper function to format messages
async def escape_mentions(member: ChatMemberUpdated, is_new: bool, text: str):
    user = member.new_chat_member.user if is_new else member.old_chat_member.user
    formatted_text = text.format(
        first=escape(user.first_name),
        last=escape(user.last_name or ""),
        username=f"@{user.username}" if user.username else mention_html(user.first_name, user.id),
        mention=mention_html(user.first_name, user.id),
        chatname=escape(member.chat.title),
        id=user.id,
    )
    return formatted_text

@app.on_chat_member_updated(filters.group)
async def welcome_goodbye_user(c: app, member: ChatMemberUpdated):
    db = Greetings(member.chat.id)

    if member.new_chat_member and member.new_chat_member.status in {CMS.MEMBER, CMS.RESTRICTED}:
        # User joined, send welcome message
        status = db.get_welcome_status()
        welcome_text = db.get_welcome_text()
        
        if status and welcome_text:
            formatted_text = await escape_mentions(member, True, welcome_text)
            await c.send_message(member.chat.id, formatted_text)
    elif member.old_chat_member and member.old_chat_member.status in {CMS.LEFT, CMS.BANNED}:
        # User left or was removed, send goodbye message
        status = db.get_goodbye_status()
        goodbye_text = db.get_goodbye_text()
        
        if status and goodbye_text:
            formatted_text = await escape_mentions(member, False, goodbye_text)
            await c.send_message(member.chat.id, formatted_text)

# Command to set welcome text
@app.on_message(filters.command("setwelcome") & filters.me)
async def set_welcome(_, m: Message):
    db = Greetings(m.chat.id)
    if not m.reply_to_message or not m.reply_to_message.text:
        await m.reply_text("Reply to a message to set as welcome text.")
        return
    db.set_welcome_text(m.reply_to_message.text)
    await m.reply_text("Welcome message saved successfully!")

# Command to set goodbye text
@app.on_message(filters.command("setgoodbye") & filters.me)
async def set_goodbye(_, m: Message):
    db = Greetings(m.chat.id)
    if not m.reply_to_message or not m.reply_to_message.text:
        await m.reply_text("Reply to a message to set as goodbye text.")
        return
    db.set_goodbye_text(m.reply_to_message.text)
    await m.reply_text("Goodbye message saved successfully!")

# Commands to toggle welcome/goodbye
@app.on_message(filters.command("welcome") & filters.me)
async def toggle_welcome(_, m: Message):
    db = Greetings(m.chat.id)
    arg = m.text.split(" ", 1)[1] if len(m.command) > 1 else ""
    if arg == "on":
        db.set_current_welcome_settings(True)
        await m.reply_text("Welcome messages enabled!")
    elif arg == "off":
        db.set_current_welcome_settings(False)
        await m.reply_text("Welcome messages disabled!")
    else:
        await m.reply_text("Use '/welcome on' or '/welcome off'.")

@app.on_message(filters.command("goodbye") & filters.me)
async def toggle_goodbye(_, m: Message):
    db = Greetings(m.chat.id)
    arg = m.text.split(" ", 1)[1] if len(m.command) > 1 else ""
    if arg == "on":
        db.set_current_goodbye_settings(True)
        await m.reply_text("Goodbye messages enabled!")
    elif arg == "off":
        db.set_current_goodbye_settings(False)
        await m.reply_text("Goodbye messages disabled!")
    else:
        await m.reply_text("Use '/goodbye on' or '/goodbye off'.")
