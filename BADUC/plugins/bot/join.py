from pyrogram import Client, filters
from BADUC.core.clients import bot
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
from pyrogram.errors import ChatAdminRequired, UserNotParticipant, ChatWriteForbidden

# List of mandatory channels/groups
MUST_JOIN = ["PBX_CHAT", "HEROKUBIN_01", "ll_BAD_ABOUT_ll", "BEAUTIFUl_DPZ", "ll_BAD_MUNDA_WORLD_ll"]

@bot.on_message(filters.incoming & filters.private, group=-1)
async def must_join_channel(bot: Client, msg: Message):
    if not MUST_JOIN:
        return

    for channel in MUST_JOIN:
        try:
            try:
                # Check if the user is a member of the channel/group
                await bot.get_chat_member(channel, msg.from_user.id)
            except UserNotParticipant:
                if channel.isalpha():
                    link = f"https://t.me/{channel}"
                else:
                    chat_info = await bot.get_chat(channel)
                    link = chat_info.invite_link

                # Ensure the link is valid before sending
                if link:
                    try:
                        await msg.reply_photo(
                            photo="https://envs.sh/Tn_.jpg",
                            caption=(
                                f"๏ ᴀᴄᴄᴏʀᴅɪɴɢ ᴛᴏ ᴍʏ ᴅᴀᴛᴀʙᴀsᴇ ʏᴏᴜ'ᴠᴇ ɴᴏᴛ ᴊᴏɪɴᴇᴅ "
                                f"[ᴊᴏɪɴ]({link}) ʏᴇᴛ. ᴘʟᴇᴀsᴇ ᴊᴏɪɴ ᴛᴏ ᴜsᴇ ᴍʏ ꜰᴇᴀᴛᴜʀᴇs."
                            ),
                            reply_markup=InlineKeyboardMarkup(
                                [[InlineKeyboardButton("Join", url=link)]]
                            )
                        )
                        await msg.stop_propagation()
                    except ChatWriteForbidden:
                        pass
        except ChatAdminRequired:
            print(f"๏ Please promote me as an admin in the chat: {channel}!")
