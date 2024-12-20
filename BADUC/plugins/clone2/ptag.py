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
