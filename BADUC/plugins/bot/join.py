from pyrogram import Client, filters
from BADUC.core.clients import bot
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
from pyrogram.errors import ChatAdminRequired, UserNotParticipant, ChatWriteForbidden

# List of mandatory channels/groups
MUST_JOIN = ["PBX_CHAT", "HEROKUBIN_01", "ll_BAD_ABOUT_ll", "BEAUTIFUl_DPZ", "ll_BAD_MUNDA_ll"]

@bot.on_message(filters.incoming & filters.private, group=-1)
async def must_join_channel(bot: Client, msg: Message):
    if not MUST_JOIN:
        return

    missing_links = []
    buttons = []

    for channel in MUST_JOIN:
        try:
            # Check if the user is a member of the channel/group
            await bot.get_chat_member(channel, msg.from_user.id)
        except UserNotParticipant:
            try:
                # Generate the invite link
                if channel.isalpha():
                    link = f"https://t.me/{channel}"
                else:
                    chat_info = await bot.get_chat(channel)
                    link = chat_info.invite_link

                # Add link and button to the list
                if link:
                    missing_links.append(link)
                    buttons.append([InlineKeyboardButton(f"Join {channel}", url=link)])
            except ChatAdminRequired:
                print(f"๏ Please promote me as an admin in the chat: {channel}!")

    # Send a single message with all missing links and buttons
    if missing_links:
        try:
            await msg.reply_photo(
                photo="https://envs.sh/Tn_.jpg",
                caption=(
                    "๏ ᴀᴄᴄᴏʀᴅɪɴɢ ᴛᴏ ᴍʏ ᴅᴀᴛᴀʙᴀsᴇ ʏᴏᴜ'ᴠᴇ ɴᴏᴛ ᴊᴏɪɴᴇᴅ ᴛʜᴇꜱᴇ ᴄʜᴀɴɴᴇʟꜱ/ɢʀᴏᴜᴘꜱ ʏᴇᴛ:\n\n"
                    + "\n".join([f"[Join {channel}]({link})" for channel, link in zip(MUST_JOIN, missing_links)])
                ),
                reply_markup=InlineKeyboardMarkup(buttons)
            )
            await msg.stop_propagation()
        except ChatWriteForbidden:
            pass
