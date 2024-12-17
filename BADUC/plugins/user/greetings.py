from pyrogram import Client, filters
from pyrogram.types import ChatMemberUpdated
from BADUC.core.clients import app


@app.on_chat_member_updated(filters.group)
def welcome_new_user(client, update: ChatMemberUpdated):
    # Check if the new user just joined the group
    if update.new_chat_member.status == "member" and update.old_chat_member.status not in ["member", "administrator", "creator"]:
        user = update.new_chat_member.user
        user_name = user.first_name or "User"
        user_id = user.id

        # Send a welcome message with user ID and name
        welcome_message = f"🌟 **Welcome to the group, [{user_name}](tg://user?id={user_id})!** 🌟"
        client.send_message(update.chat.id, welcome_message)
