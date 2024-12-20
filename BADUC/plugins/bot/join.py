from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
from pyrogram.errors import ChatAdminRequired, UserNotParticipant, ChatWriteForbidden
from BADUC.core.clients import bot
from BADUC.core.config import MUST_JOIN_GROUPS

@bot.on_message(filters.incoming & filters.private, group=-1)
async def must_join_channels(bot: Client, msg: Message):
    if not MUST_JOIN_GROUPS or len(MUST_JOIN_GROUPS) < 5:
        return
    
    not_joined_links = []

    for group in MUST_JOIN_GROUPS:
    try:
        await bot.get_chat_member(group, msg.from_user.id)
    except UserNotParticipant:
        try:
            chat_info = await bot.get_chat(group)
            link = chat_info.invite_link if not group.isalpha() else f"https://t.me/{group}"
            not_joined_links.append(link)
        except Exception as e:
            print(f"Error accessing group {group}: {e}")
    
    if not_joined_links:
        buttons = [
            [InlineKeyboardButton(f"Join Group {i+1}", url=link)]
            for i, link in enumerate(not_joined_links)
        ]
        try:
            await msg.reply_photo(
                photo="https://envs.sh/Tn_.jpg",
                caption=(
                    f"👋 ʜᴇʟʟᴏ  **{msg.from_user.mention},**\n\n"
                    "⚜️ʏᴏᴜ ɴᴇᴇᴅ ᴛᴏ ᴊᴏɪɴ ᴀʟʟ ᴛʜᴇ ʀᴇQᴜɪʀᴇᴅ ɢʀᴏᴜᴘꜱ ᴛᴏ ᴜꜱᴇ ᴛʜɪꜱ ʙᴏᴛ❤️\n\n"
                    "💫 ᴘʟᴇᴀꜱᴇ ᴊᴏɪɴ ᴛʜᴇ ꜰᴏʟʟᴏᴡɪɴɢ ɢʀᴏᴜᴘꜱ🪄"
                ),
                reply_markup=InlineKeyboardMarkup(buttons),
            )
            await msg.stop_propagation()
        except ChatWriteForbidden:
            pass
    else:
        pass
        
