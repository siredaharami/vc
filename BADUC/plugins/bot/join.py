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

    missing_channels = []  # To store missing channel names
    buttons = []  # To store button objects

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
                    missing_channels.append(channel)
                    buttons.append([InlineKeyboardButton(f"ᴊᴏɪɴ {channel}", url=link)])
            except ChatAdminRequired:
                print(f"๏ ᴘʟᴇᴀꜱᴇ ᴘʀᴏᴍᴏᴛᴇ ᴍᴇ ᴀꜱ ᴀɴ ᴀᴅᴍɪɴ ɪɴ ᴛʜᴇ ᴄʜᴀᴛ {channel}!")

    # Send a single message with all missing links and buttons
    if missing_channels:
        try:
            # Make sure all buttons are added to the InlineKeyboardMarkup
            await msg.reply_photo(
                photo="https://files.catbox.moe/2kporf.jpg",
                caption=(
                    "๏ ᴀᴄᴄᴏʀᴅɪɴɢ ᴛᴏ ᴍʏ ᴅᴀᴛᴀʙᴀsᴇ, ʏᴏᴜ'ᴠᴇ ɴᴏᴛ ᴊᴏɪɴᴇᴅ ᴛʜᴇꜱᴇ ᴄʜᴀɴɴᴇʟꜱ/ɢʀᴏᴜᴘꜱ ʏᴇᴛ:\n\n"
                    + "\n".join([f"[ᴊᴏɪɴ {channel}](https://t.me/{channel})" for channel in missing_channels])
                ),
                reply_markup=InlineKeyboardMarkup(buttons)
            )
            await msg.stop_propagation()
        except ChatWriteForbidden:
            pass
