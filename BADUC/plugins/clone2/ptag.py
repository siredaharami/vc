from pyrogram import Client, filters
from pyrogram.enums import ChatType, ChatMemberStatus
from pyrogram.errors import UserNotParticipant
import asyncio
import random

from BADUC.plugins.bot.clone3 import get_bot_owner  # Import the function to check bot owner

spam_chats = []

EMOJI = [ "🦋🦋🦋🦋🦋",
          "🧚🌸🧋🍬🫖",
          "🥀🌷🌹🌺💐",
          "🌸🌿💮🌱🌵",
          "❤️💚💙💜🖤",
          "💓💕💞💗💖",
          "🌸💐🌺🌹🦋",
          "🍔🦪🍛🍲🥗",
          "🍎🍓🍒🍑🌶️",
          "🧋🥤🧋🥛🍷",
          "🍬🍭🧁🎂🍡",
          "🍨🧉🍺☕🍻",
          "🥪🥧🍦🍥🍚",
          "🫖☕🍹🍷🥛",
          "☕🧃🍩🍦🍙",
          "🍁🌾💮🍂🌿",
          "🌨️🌥️⛈️🌩️🌧️",
          "🌷🏵️🌸🌺💐",
          "💮🌼🌻🍀🍁",
          "🧟🦸🦹🧙👸",
          "🧅🍠🥕🌽🥦",
          "🐷🐹🐭🐨🐻‍❄️",
          "🦋🐇🐀🐈🐈‍⬛",
          "🌼🌳🌲🌴🌵",
          "🥩🍋🍐🍈🍇",
          "🍴🍽️🔪🍶🥃",
          "🕌🏰🏩⛩️🏩",
          "🎉🎊🎈🎂🎀",
          "🪴🌵🌴🌳🌲",
          "🎄🎋🎍🎑🎎",
          "🦅🦜🕊️🦤🦢",
          "🦤🦩🦚🦃🦆",
          "🐬🦭🦈🐋🐳",
          "🐔🐟🐠🐡🦐",
          "🦩🦀🦑🐙🦪",
          "🐦🦂🕷️🕸️🐚",
          "🥪🍰🥧🍨🍨",
          " 🥬🍉🧁🧇",
]

TAGMES = [ " ʜᴇʏ ʙᴀʙʏ ᴋᴀʜᴀ ʜᴏ🤗🥱 ",
           " ᴏʏᴇ sᴏ ɢʏᴇ ᴋʏᴀ ᴏɴʟɪɴᴇ ᴀᴀᴏ😊 ",
           " ᴠᴄ ᴄʜᴀʟᴏ ʙᴀᴛᴇɴ ᴋᴀʀᴛᴇ ʜᴀɪɴ ᴋᴜᴄʜ ᴋᴜᴄʜ😃 ",
           " ᴋʜᴀɴᴀ ᴋʜᴀ ʟɪʏᴇ ᴊɪ..??🥲 ",
           " ɢʜᴀʀ ᴍᴇ sᴀʙ ᴋᴀɪsᴇ ʜᴀɪɴ ᴊɪ🥺 ",
           " ᴘᴛᴀ ʜᴀɪ ʙᴏʜᴏᴛ ᴍɪss ᴋᴀʀ ʀʜɪ ᴛʜɪ ᴀᴀᴘᴋᴏ🤭 ",
           " ᴏʏᴇ ʜᴀʟ ᴄʜᴀʟ ᴋᴇsᴀ ʜᴀɪ..??🤨 ",
           " ᴍᴇʀɪ ʙʜɪ sᴇᴛᴛɪɴɢ ᴋᴀʀʙᴀ ᴅᴏɢᴇ..??🙂 ",
           " ᴀᴀᴘᴋᴀ ɴᴀᴍᴇ ᴋʏᴀ ʜᴀɪ..??🥲 ",
           " ɴᴀsᴛᴀ ʜᴜᴀ ᴀᴀᴘᴋᴀ..??😋 ",
           " ᴍᴇʀᴇ ᴋᴏ ᴀᴘɴᴇ ɢʀᴏᴜᴘ ᴍᴇ ᴋɪᴅɴᴀᴘ ᴋʀ ʟᴏ😍 ",
           " ᴀᴀᴘᴋɪ ᴘᴀʀᴛɴᴇʀ ᴀᴀᴘᴋᴏ ᴅʜᴜɴᴅ ʀʜᴇ ʜᴀɪɴ ᴊʟᴅɪ ᴏɴʟɪɴᴇ ᴀʏɪᴀᴇ😅😅 ",
           " ᴍᴇʀᴇ sᴇ ᴅᴏsᴛɪ ᴋʀᴏɢᴇ..??🤔 ",
           " sᴏɴᴇ ᴄʜᴀʟ ɢʏᴇ ᴋʏᴀ🙄🙄 ",
           " ᴇᴋ sᴏɴɢ ᴘʟᴀʏ ᴋʀᴏ ɴᴀ ᴘʟss😕 ",
           " ᴀᴀᴘ ᴋᴀʜᴀ sᴇ ʜᴏ..??🙃 ",
           " ʜᴇʟʟᴏ ᴊɪ ɴᴀᴍᴀsᴛᴇ😛 ",
           " ʜᴇʟʟᴏ ʙᴀʙʏ ᴋᴋʀʜ..?🤔 ",
           " ᴅᴏ ʏᴏᴜ ᴋɴᴏᴡ ᴡʜᴏ ɪs ᴍʏ ᴏᴡɴᴇʀ.? ",
           " ᴄʜʟᴏ ᴋᴜᴄʜ ɢᴀᴍᴇ ᴋʜᴇʟᴛᴇ ʜᴀɪɴ.🤗 ",
           " ᴀᴜʀ ʙᴀᴛᴀᴏ ᴋᴀɪsᴇ ʜᴏ ʙᴀʙʏ😇 ",
           " ᴛᴜᴍʜᴀʀɪ ᴍᴜᴍᴍʏ ᴋʏᴀ ᴋᴀʀ ʀᴀʜɪ ʜᴀɪ🤭 ",
           " ᴍᴇʀᴇ sᴇ ʙᴀᴛ ɴᴏɪ ᴋʀᴏɢᴇ🥺🥺 ",
           " ᴏʏᴇ ᴘᴀɢᴀʟ ᴏɴʟɪɴᴇ ᴀᴀ ᴊᴀ😶 ",
           " ᴀᴀᴊ ʜᴏʟɪᴅᴀʏ ʜᴀɪ ᴋʏᴀ sᴄʜᴏᴏʟ ᴍᴇ..??🤔 ",
           " ᴏʏᴇ ɢᴏᴏᴅ ᴍᴏʀɴɪɴɢ😜 ",
           " sᴜɴᴏ ᴇᴋ ᴋᴀᴍ ʜᴀɪ ᴛᴜᴍsᴇ🙂 ",
           " ᴋᴏɪ sᴏɴɢ ᴘʟᴀʏ ᴋʀᴏ ɴᴀ😪 ",
           " ɴɪᴄᴇ ᴛᴏ ᴍᴇᴇᴛ ᴜʜ☺ ",
           " ʜᴇʟʟᴏ🙊 ",
           " sᴛᴜᴅʏ ᴄᴏᴍʟᴇᴛᴇ ʜᴜᴀ??😺 ",
           " ʙᴏʟᴏ ɴᴀ ᴋᴜᴄʜ ʏʀʀ🥲 ",
           " sᴏɴᴀʟɪ ᴋᴏɴ ʜᴀɪ...??😅 ",
           " ᴛᴜᴍʜᴀʀɪ ᴇᴋ ᴘɪᴄ ᴍɪʟᴇɢɪ..?😅 ",
           " ᴍᴜᴍᴍʏ ᴀᴀ ɢʏɪ ᴋʏᴀ😆😆😆 ",
           " ᴏʀ ʙᴀᴛᴀᴏ ʙʜᴀʙʜɪ ᴋᴀɪsɪ ʜᴀɪ😉 ",
           " ɪ ʟᴏᴠᴇ ʏᴏᴜ🙈🙈🙈 ",
           " ᴅᴏ ʏᴏᴜ ʟᴏᴠᴇ ᴍᴇ..?👀 ",
           " ʀᴀᴋʜɪ ᴋᴀʙ ʙᴀɴᴅ ʀᴀʜɪ ʜᴏ.??🙉 ",
           " ᴇᴋ sᴏɴɢ sᴜɴᴀᴜ..?😹 ",
           " ᴏɴʟɪɴᴇ ᴀᴀ ᴊᴀ ʀᴇ sᴏɴɢ sᴜɴᴀ ʀᴀʜɪ ʜᴜ😻 ",
           " ɪɴsᴛᴀɢʀᴀᴍ ᴄʜᴀʟᴀᴛᴇ ʜᴏ..??🙃 ",
           " ᴡʜᴀᴛsᴀᴘᴘ ɴᴜᴍʙᴇʀ ᴅᴏɢᴇ ᴀᴘɴᴀ ᴛᴜᴍ..?😕 ",
           " ᴛᴜᴍʜᴇ ᴋᴏɴ sᴀ ᴍᴜsɪᴄ sᴜɴɴᴀ ᴘᴀsᴀɴᴅ ʜᴀɪ..?🙃 ",
           " sᴀʀᴀ ᴋᴀᴍ ᴋʜᴀᴛᴀᴍ ʜᴏ ɢʏᴀ ᴀᴀᴘᴋᴀ..?🙃 ",
           " ᴋᴀʜᴀ sᴇ ʜᴏ ᴀᴀᴘ😊 ",
           " sᴜɴᴏ ɴᴀ🧐 ",
           " ᴍᴇʀᴀ ᴇᴋ ᴋᴀᴀᴍ ᴋᴀʀ ᴅᴏɢᴇ..? ",
           " ʙʏ ᴛᴀᴛᴀ ᴍᴀᴛ ʙᴀᴛ ᴋᴀʀɴᴀ ᴀᴀᴊ ᴋᴇ ʙᴀᴅ😠 ",
           " ᴍᴏᴍ ᴅᴀᴅ ᴋᴀɪsᴇ ʜᴀɪɴ..?❤ ",
           " ᴋʏᴀ ʜᴜᴀ..?👱 ",
           " ʙᴏʜᴏᴛ ʏᴀᴀᴅ ᴀᴀ ʀʜɪ ʜᴀɪ 🤧❣️ ",
           " ʙʜᴜʟ ɢʏᴇ ᴍᴜᴊʜᴇ😏😏 ",
           " ᴊᴜᴛʜ ɴʜɪ ʙᴏʟɴᴀ ᴄʜᴀʜɪʏᴇ🤐 ",
           " ᴋʜᴀ ʟᴏ ʙʜᴀᴡ ᴍᴀᴛ ᴋʀᴏ ʙᴀᴀᴛ😒 ",
           " ᴋʏᴀ ʜᴜᴀ😮😮 ",
           " ʜɪɪ👀 ",
           " ᴀᴀᴘᴋᴇ ᴊᴀɪsᴀ ᴅᴏsᴛ ʜᴏ sᴀᴛʜ ᴍᴇ ғɪʀ ɢᴜᴍ ᴋɪs ʙᴀᴛ ᴋᴀ 🙈 ",
           " ᴀᴀᴊ ᴍᴀɪ sᴀᴅ ʜᴜ ☹️ ",
           " ᴍᴜsᴊʜsᴇ ʙʜɪ ʙᴀᴛ ᴋᴀʀ ʟᴏ ɴᴀ 🥺🥺 ",
           " ᴋʏᴀ ᴋᴀʀ ʀᴀʜᴇ ʜᴏ👀 ",
           " ᴋʏᴀ ʜᴀʟ ᴄʜᴀʟ ʜᴀɪ 🙂 ",
           " ᴋᴀʜᴀ sᴇ ʜᴏ ᴀᴀᴘ..?🤔 ",
           " ᴄʜᴀᴛᴛɪɴɢ ᴋᴀʀ ʟᴏ ɴᴀ..🥺 ",
           " ᴍᴇ ᴍᴀsᴏᴏᴍ ʜᴜ ɴᴀ🥺🥺 ",
           " ʏᴀʜᴀ ᴀᴀ ᴊᴀᴏ:-[@PBX_CHAT]  ᴍᴀꜱᴛɪ ᴋᴀʀᴇɴɢᴇ 🤭🤭 ",
           " ᴛʀᴜᴛʜ ᴀɴᴅ ᴅᴀʀᴇ ᴋʜᴇʟᴏɢᴇ..? 😊 ",
           " ᴀᴀᴊ ᴍᴜᴍᴍʏ ɴᴇ ᴅᴀᴛᴀ ʏʀ🥺🥺 ",
           " ᴊᴏɪɴ ᴋᴀʀ ʟᴏ🤗 ",
           " ᴇᴋ ᴅɪʟ ʜᴀɪ ᴇᴋ ᴅɪʟ ʜɪ ᴛᴏ ʜᴀɪ😗😗 ",
           " ᴛᴜᴍʜᴀʀᴇ ᴅᴏꜱᴛ ᴋᴀʜᴀ ɢʏᴇ🥺 ",
           " ᴍʏ ᴄᴜᴛᴇ ᴏᴡɴᴇʀ{ @ll_BAD_MUNDA_ll}🥰 ",
           " ᴋᴀʜᴀ ᴋʜᴏʏᴇ ʜᴏ ᴊᴀᴀɴ😜 ",
           " ɢᴏᴏᴅ ɴ⁸ ᴊɪ ʙʜᴜᴛ ʀᴀᴛ ʜᴏ ɢʏɪ🥰 ",
         ]

GGM_TAG = [ "**ਗੁੱਡ ਮੋਰਨਿੰਗ 💘🌷**",
"ਗੁੱਡ ਮੋਰਨਿੰਗ 👀🕊️**",
"ਗੁੱਡ ਮੋਰਨਿੰਗ 🌾💸**",
"ਗੁੱਡ ਮੋਰਨਿੰਗ ☕🍩**",
"ਗੁੱਡ ਮੋਰਨਿੰਗ 👀🇺🇲**",
"ਗੁੱਡ ਮੋਰਨਿੰਗ 🍼😚**",
"ਗੁੱਡ ਮੋਰਨਿੰਗ 😍😘**",
"ਗੁੱਡ ਮੋਰਨਿੰਗ ਮੇਰੀ ਜਾਣ👀😚**",
"ਹਾਂਜੀ ਗੁੱਡ ਮੋਰਨਿੰਗ ਸੋਣਯੋ 🫶🏻😍**",
"ਉਠੋ ਜੀ 😿💘**",
"ਤੁਸੀ ਉਠੇ ਨਹੀਂ ਹਲੇ 😿😍**",        
]

GGN_TAG = [ "**ਗੁੱਡ ਨਾਈਟ 🥱🫢**",
"**ਸੋਜੋਂ ਜੀ 🤗😴**",
"**ਰਾਤ ਹੋਗੀ ਜੀ ਨਿਨਿ ਕਰਲੋ 💘😚**",
"**ਤੁਸੀ ਹਲੇ ਸੁੱਤੇ ਨਹੀਂ 🙀😾**",
"**ਹਾਂਜੀ ਕਦੋ ਸੌਣਾ ਫੇਰ 👀🫶🏻**",
"**ਰਖਦੋ ਫੋਨ ਸੋਜੋ ਛੇਤੀ 💘😘**",
"**ਛੇਤੀ ਸੋਜਯੋ ਨਹੀਂ ਤੇ ਮਾਉ ਆਜੁ 🙀👽**",
"**ਤੁਸੀ ਕਦੋ ਸੋਵੋਗੇ 😢😮‍💨**",
"**ਗੁੱਡ ਨਾਈਟ ਜੀ 💘 ਬਬ ਜੂ 🤗**",
]

CCHAT_TAG = [ "**ਤੁਸੀ ਕਿੱਥੇ ਓ 👀☹️**",

"**ਆਜੋ ਗਲਾ ਕਰੀਏ 😺🫠**",

"**ਕੋਈ ਤੇ ਚੈਟ ਕਰਨ ਨੁ ਆਜੋ 🕊️🥲**",

"**ਕਿੱਥੇ ਓ 𝐁𝐔𝐒𝐘 ਬੰਦਿਓ 🌜🌛**",

"**ਤੁਸੀ ਕਿੱਥੇ ਓ 🥲 ਮੇ ਉਡੀਕ ਕਰ ਕੇ ਥੱਕ ਗਿਆ 😾**",

"**ਤੁਸੀ ਗਲਾ ਕਰਦੇ ਨਹੀਂ 😮‍💨 ਅਸੀ ਵਾਕੇ ਕਰਨੇ ਆ 😾**",

"**ਆਜਾ ਛੇੜੀਏ ਬਾਤੜੀਆ 🙈 ਬੋਹਤੀ ਦੇਰ ਨਾ ਲਾਯੋ ਜੀ 💘**",

"**ਦਿੱਲ ਕਰੇ ਤੇਰੇ ਨਲ ਗਲ ਕਰਨ ਦਾ 💞 grp ਦੇ ਵਿਚ ਗੇੜਾ ਮਾਰ ਕੁੜੇ 🕊️**",

"**𝐆𝐑𝐏 ਚ ਆਓਗੇ 💘 ਕੇ 𝐃𝐌 ਕਰਲੀਏ**",

"** ਆਜਾ ਮੇਰੇ ਬਟੁਰੇ 🤭ਕਿੱਥੇ ਰਹਿ ਗਿਆ❤️ **",
            
"** ਬਾਹ ਫੜ੍ਹ 🫣 ਤੈਨੂੰ ਗੇੜਾ ਲਵਾਇਏ ਗਰੁੱਪ ਦਾ😜 **",
            
"** ਆ ਗੰਦਾ 😕 ਜਿਹਾ ਗਲੂਪ ਆ ਇਥੇ ਆਜੋ 🙈[ @ll_BAD_GROUP_ll ] 😚 **",
            
"** ਮੇਰਾ ਨੋਨਾ 😍 ਓਨਵਰ [ @ll_BAD_MUNDA_ll ] 🥰 **",
            
"** ਆਜਾ ਬਾਤਾ 😚ਪਾਈਏ ਰਲਕੇ 👻 **",
            
"** ਅਕੜ ਬਕੜ ⚡ ਬੰਬੇ ਬੌ ਆਜਾ ਜਮੀਏ ਆਪਣੇ ਨਿਆਣੇ ਦੋ🙉 **",
            
"** ਆਜਾ ਚੰਦਰੀਏ 🙊 ਭੜਿਕੇ ਪਾਈਏ ਦਿਲਾ ਦੇ ❤️ **",
            
"** ਦੂਜੇ ਗਰੁੱਪਾਂ 😒ਚ ਕਿ ਕਰਦੀ ਇੱਥੇ ਵੀ ਫੇਰਾ ਪਾਜਾ 😕 **",
            
"** ਆਜਾ ਬੇਬੀ ਬੋਰੀਅਤ 🤓 ਦੀ ਜੜ ਤੋੜੀਏ ਦੋਵੇਂ ਰਲਕੇ ਗੱਲਾਂ ਅੱਗੇ ਤੋਰੀਏ 🥳 **",
            
"** ਆਜਾ ਪਾਂ ਲੀਏ ਜੇਬੀ 🌹 ਚ ਤੇਨੂੰ ਕਿੱਥੇ ਭਜਦੀ 🐒 **",
            
"** ਚਲ ਛਿਪ ਗਿਆ 🌚 ਚੰਨ ਹੋ ਗਿਆ ਸਵੇਰਾ ਪਾਂ ਜਾ ਮੇਰੇ ਸੁਪਨਿਆਂ ਚ ਫੇਰਾ 👻 **",  
            
 ]

# Helper function to check authorization
async def is_authorized(client, message):
    bot_info = await client.get_me()
    bot_id = bot_info.id
    user_id = message.from_user.id
    owner_id = await get_bot_owner(bot_id)
    if owner_id != user_id:
        await message.reply_text("❌ You're not authorized to use this bot.")
        return False
    return True

@Client.on_message(filters.command(["pgmtag"], prefixes=["/"]))
async def mention_allvc(client, message):
    if not await is_authorized(client, message):
        return
    
    chat_id = message.chat.id
    if message.chat.type == ChatType.PRIVATE:
        return await message.reply("๏ This command only works in groups.")

    if chat_id in spam_chats:
        return await message.reply("๏ Please stop the previous mention process first.")
    
    spam_chats.append(chat_id)
    usrnum = 0
    usrtxt = ""
    async for usr in client.get_chat_members(chat_id):
        if not chat_id in spam_chats:
            break
        if usr.user.is_bot:
            continue
        usrnum += 1
        usrtxt += f"[{usr.user.first_name}](tg://user?id={usr.user.id}) "

        if usrnum == 1:
            txt = f"{usrtxt} {random.choice(GGM_TAG)}"
            await client.send_message(chat_id, txt)
            await asyncio.sleep(4)
            usrnum = 0
            usrtxt = ""
    try:
        spam_chats.remove(chat_id)
    except:
        pass

@Client.on_message(filters.command(["pgntag"], prefixes=["/"]))
async def mention_night(client, message):
    if not await is_authorized(client, message):
        return
    
    chat_id = message.chat.id
    if message.chat.type == ChatType.PRIVATE:
        return await message.reply("๏ This command only works in groups.")

    if chat_id in spam_chats:
        return await message.reply("๏ Please stop the previous mention process first.")
    
    spam_chats.append(chat_id)
    usrnum = 0
    usrtxt = ""
    async for usr in client.get_chat_members(chat_id):
        if not chat_id in spam_chats:
            break
        if usr.user.is_bot:
            continue
        usrnum += 1
        usrtxt += f"[{usr.user.first_name}](tg://user?id={usr.user.id}) "

        if usrnum == 1:
            txt = f"{usrtxt} {random.choice(GGN_TAG)}"
            await client.send_message(chat_id, txt)
            await asyncio.sleep(4)
            usrnum = 0
            usrtxt = ""
    try:
        spam_chats.remove(chat_id)
    except:
        pass

@Client.on_message(filters.command(["ptag"], prefixes=["/"]))
async def mention_chat(client, message):
    if not await is_authorized(client, message):
        return
    
    chat_id = message.chat.id
    if message.chat.type == ChatType.PRIVATE:
        return await message.reply("๏ This command only works in groups.")

    if chat_id in spam_chats:
        return await message.reply("๏ Please stop the previous mention process first.")
    
    spam_chats.append(chat_id)
    usrnum = 0
    usrtxt = ""
    async for usr in client.get_chat_members(chat_id):
        if not chat_id in spam_chats:
            break
        if usr.user.is_bot:
            continue
        usrnum += 1
        usrtxt += f"[{usr.user.first_name}](tg://user?id={usr.user.id}) "

        if usrnum == 1:
            txt = f"{usrtxt} {random.choice(CCHAT_TAG)}"
            await client.send_message(chat_id, txt)
            await asyncio.sleep(4)
            usrnum = 0
            usrtxt = ""
    try:
        spam_chats.remove(chat_id)
    except:
        pass

@Client.on_message(filters.command(["tagall"], prefixes=["/"]))
async def mention_allvc(client, message):
    if not await is_authorized(client, message):
        return
    
    chat_id = message.chat.id
    if message.chat.type == ChatType.PRIVATE:
        return await message.reply("๏ This command only works in groups.")

    if chat_id in spam_chats:
        return await message.reply("๏ Please stop the previous mention process first.")
    
    spam_chats.append(chat_id)
    usrnum = 0
    usrtxt = ""
    async for usr in client.get_chat_members(chat_id):
        if not chat_id in spam_chats:
            break
        if usr.user.is_bot:
            continue
        usrnum += 1
        usrtxt += f"[{usr.user.first_name}](tg://user?id={usr.user.id}) "

        if usrnum == 1:
            txt = f"{usrtxt} {random.choice(TAGMES)}"
            await client.send_message(chat_id, txt)
            await asyncio.sleep(4)
            usrnum = 0
            usrtxt = ""
    try:
        spam_chats.remove(chat_id)
    except:
        pass

@Client.on_message(filters.command(["pgmstop", "pgnstop", "pvcstop", "allstop"]))
async def cancel_spam(client, message):
    if not await is_authorized(client, message):
        return
    
    if message.chat.id not in spam_chats:
        return await message.reply("๏ Currently, I'm not tagging anyone.")
    
    try:
        spam_chats.remove(message.chat.id)
    except:
        pass
    return await message.reply("๏ Mention process stopped.")
