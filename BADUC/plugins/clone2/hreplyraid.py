import random
import asyncio

from pyrogram import Client, filters
from pyrogram.enums import MessageEntityType as MET, ChatAction as CA
from pyrogram.types import Message
from BADUC.plugins.bot.clone3 import get_bot_owner

#HIREPLYRAID


HRAID_STR = [
   "मादरचोद तेरी माँ की चूत में घुटका खाके थूक दूंगा 🤣🤣", 
    "मादरचोद तेरी माँ की चूत में घुटका खाके थूक दूंगा 🤣🤣", 
    "तेरे बहन की चूत में चाकू डाल कर चूत का खून कर दूँगा", 
    "तेरी माँ की चूत में शैतान का लौड़ा 🤣🤣",
    "तेरी वहीं नहीं है क्या? 9 महीने रुक सगी वहीं देता हूं 🤣🤣🤩",
    "तेरी मां के भोसड़े में एयरोप्लेनपार्क करके उड़ान भर दूंगा ✈️🛫",
    "तेरी मां की चूत में सुतली बम फोड़ दूंगा तेरी माँ की झाटे जल के खाक हो जाएगी💣",
    "तेरी माँ की चूत में स्कूटर डाल दूँगा👅","तेरी माँ की चूत में शैतान का लौड़ा 🤣🤣",
    "तेरे बहन की चूत में चाकू डाल कर चूत का खून कर दुगा",
    "तेरे बहन की चूत में चाकू डाल कर चूत का खून कर दूंगा",
    "तेरी माँ की चूत 🤱गली के कुट्टो 🦮मैं बात दूँगा फिर 🍞ब्रेड की तरह खाएँगे वो तेरी माँ की चूत",
    "दूध हिलाऊंगा तेरी दीवारों के ऊपर नीचे 🆙🆒😙",
    "तेरी मां की चूत में ✋ हत्थ डालके 👶 बच्चे निकाल दूंगा 😍",
    "तेरी बहन की चूत में काले के छिलके 🍌🍌😍",
    "तेरी बहन की चूत में यूजरबोट लू अगाउंगा सस्ते स्पैम के छोड़े",
    "तेरी वहीं धंधे वाली 😋😛",
    "तेरी मां के भोसड़े में एसी लगा दूंगा सारी गर्मी निकल जाएगी",
    "तेरी कारों को हॉर्लिक्स पिलाऊंगा मादरचोद😚",
    "तेरी मां की चूत में शैतान का लौड़ा 🤣🤣 ",
    "तेरी मां की गांड में सरिया डाल दूंगा मादरचोद उसी साड़ी में पीआर टांग के बच्चे पैदा होंगे 😱😱",
    "तेरी मां को कोलकाता वाले जीतू भैया का लंड मुबारक 🤩🤩","तेरी मां की फैंटेसी हूं बेटे, तू अपनी बहन को संभाल 😈😈",
    "तेरा पहला बाप हूं मादरचोद","तेरी वही के भोसड़े में XVIDEOS.COM चला के मुंह मारूंगा 🤡😹",
    "तेरी मां का ग्रुप वालों साथ मिलके गैंग बैंग करूंगा🙌🏻☠️",
    "तेरी आइटम कि गांड में लंड डालके, तेरे जैसा एक या निकाल दूंगा मादरचोद🤘🏻🙌🏻☠️ ",
    "औकात में रह वरना गांड में डंडा डाल के मुंह से निकाल दूंगा शरीर भी डंडे जैसा दिखेगा 🙄🤭🤭",
    "तेरी मां मेरे साथ लूडो खेलते-खेलते उसके मुंह में अपना लोडा दे दूंगा☝🏻☝🏻😬",
    "तेरी योनि को अपने लंड पर इतना झूलाउंगा कि झूलते-झूलते ही बच्चा पैदा कर देगी👀👯",
    "तेरी मां की चूत में बैटरी लगा के पावरबैंक बना डी यूएनजीए 🔋 🔥🤩",
    "तेरी मां की चूत में सी स्ट्रिंग एन्क्रिप्शन लगा दूंगा बहुत हुई छुट रुक जाएगीIII😈🔥😍",
    "तेरी मां के गांड में झाड़ू दाल के मोर 🦚बना दूंगा 🤩🥵😱",
    "तेरी मां के गांड में झाड़ू डाल के मोर 🦚बना दूंगा 🤩🥵😱",
    "तेरी मां के गांड में झाड़ू डाल के मोर 🦚बना दूंगा 🤩🥵😱",
    "तेरी मां के चूत में थानेदार उल्डरिंग कर दूंगा हिलते हुए भी दर्द होगा😱🤮👺",
    "तेरी मां को रेडी पे बैठल के उसकी उसकी चूत बिलवाउंगा 💰 😵🤩",
    "भोसदिके तेरी मां की चूत में 4 होले है उनमे मसील लगा बहुत लगती है भोफडीके 👊🤮🤢🤢 ",
    "तेरी बहन की चूत में बरगद का पेड़ उगा दूंगा कोरोना में सब ऑक्सीजन लेकर जाएंगे🤢🤩🥳",
    "तेरी मां की चूत में सूडो लगा के बिगस्पम लगा के 9999 चोद लगा दू 🤩🥳🔥",
    "तेरी बहन के भो ओएसडाइक मैं बेसन के लड्डू भर दूंगा🤩🥳🔥😈",
    "तेरी मां की चूत खोद के उसे सिलेंडर ⛽️ फिट करके हमें दाल मखनी बनाऊंगा🤩👊🔥",
    "तेरी मां की चूत में शीशा दाल दूंगा और चौराहे पे तांग डूंगा भोसडाइक😈😱 🤩",
    "तेरी मां की चूत में क्रेडिट कार्ड डाल के उम्र से 500 साल पहले नोट निकालूंगा भोसड़ाके💰💰🤩",
    "तेरी मां के साथ सुर का सेक्स करवा दूंगा एक साथ 6-6 बच्चे देगी💰🔥😱",
    " तेरी बहन की चूत में एप्पल का 18W वाला चार्जर 🔥🤩",
    "तेरी बहन की गांड में वनप्लस का रैप चार्जर 30W हाई पावर 💥😂😎",
    "तेरी बहन की चूत को अमेज़न से ऑर्डर करुंगा 10 रुपये में और फ्लिप एआरटी पीई 20 रुपये मेई बेक डुंगा 🤮👿😈🤖 वीओ एक या फ्री डिलीवरी देगी🙀👍🥳🔥",
    "तेरी बहन की चूत काली🙁🤣💥",
    "तेरी मां की चूत में बदलाव के लिए प्रतिबद्ध हूं, तेरी बहन की चूत अपने आप अपडेट हो जाएगी🤖🙏🤔",
    "तेरी मौसी के भोसडे मेई इंडियन रेलवे 🚂💥😂",
    "तू तेरी बहन तेरा खानदान सब बहन के लौड़े रंडी है रंडी 🤢✅🔥",
    "तेरी बहन की चूत में आयनिक बॉन्ड बना के वर्जिनिटी लूज करवा दूंगा उसकी 📚 😎🤩",
    "टेर मैं रंडी माँ से पूछना बाप का नाम बहनों के लोदी 🤩🥳😳",
    "तू और तेरी मां दोनों की भोसड़े में मेट्रो चलवा दूंगा मादरचोद 🚇🤩😱🥶",
    "तेरी मां को इतना चोदूंगा तेरा बाप भी उसको पहचानने से मना कर देगा 😂👿🤩 ",
    "तेरी बहन के भोसड़े में हेयर ड्रायर चला दूंगा💥🔥🔥",
    "तेरी मां की चूत में टेलीग्राम की सारी रंडियों का रंडी खाना खोल दूंगा👿🤮😎",
    "तेरी मां की चूत एलेक्सा डाल की डीजे बजाऊंगा 🎶 ⬆️🤩 💥",
    "तेरी माँ के भोसड़े में गिठब डाल के अपना बोट होस्ट करुंगा 🤩👊👤😍",
    "तेरी बहन का वीपीएस बना के 24*7 बैश चुदाई कमांड दे दूंगा 🤩💥🔥🔥",
    "तेरी माँ की चूत में तेरे लंड को डाल के काट दूंगा मादरचोद 🔪😂🔥",
    "सुन तेरी मां का भोसड़ा और तेरी बहन का भी भोसड़ा 👿😎👊",
    "तुझे देख के तेरी रंडी बहन पे तरस आता है मुझे बहन के लौड़े 👿 💥🤩🔥",
    "सुन मादरचोद ज्यादा न उछल मां चोद देंगे एक मिनट में ✅🤣🔥🤩",
    "अपनी अम्मा से पूछना उसको हमें काली रात में कौन चोदने आया था!",
    "तेरी वहीं नहीं है क्या? 9 महीने रुक ꜱअगी वहीं देता हूं 🤣🤣🤩", 
    "तेरी मां के भोꜱदे में एयरोप्लेनपार्क करके उड़ान भर दूंगा ✈️🛫",
    "तेरी मां की चूत में ꜱउटली बम फोड दूंगा तेरी मां की झाटे जल के खाक हो जाएगी💣",
    "तेरी माँ की चूत में ꜱकूटर डाल दूँगा👅",
    "तेरी माँ की चूत 🤱गली के कुत्ते 🦮मैं बात दूँगा फिर 🍞रोटी की तरह खाएँगे वो तेरी माँ की चूत",
    "दूध हिलाऊँगा तेरी वहीं के यूपीआर आला 🆙🆒😙",
    "तेरी माँ की चूत में ✋हत्थ डालके 👶बच्चे निकाल दूंगा 😍",
    "तेरी बहन की चूत में काले के छिलके 🍌🍌😍",
    "तेरी बहन की चूत में उꜱएरबोट लगाऊंगा ꜱaꜱते ꜱपम के चोदे" ,
    "तेरी वहीं धंधे वाली 😋😛", 
    "तेरी मां के भोकडे में एसी लगा दूंगा ꜱरी गर्मी निकल जाएगी",
    "तेरी वहीं को हॉर्लिकꜱ पीलूंगा मादरचोद😚", 
    "तेरी मां की गांड में ꜱअरिया डाल दूंगा मादरचोद uꜱi ꜱariye pr तांग के बच्चे पैदा होंगे 😱😱",
    "तेरी मां को कोलकाता वाले जीतू भैया का लंड मुबारक 🤩🤩",
    "तेरी मम्मी की फैन्टसी हूं बेटे, तू अपनी बहन को ꜱप्रभाल 😈😈",
    "तेरा पहला बाप हूं मादरचोद",
    "तेरी वहीं ke bhoꜱde me xvideoꜱ.com चला के मुंह मारूंगा 🤡😹",
    "तेरी मां का ग्रुप वालों ꜱसाथ मिलके गैंग बैंग करूंगा🙌🏻☠️",
    "तेरी आइटम की गांड में लंड डालके,तेरे जयꜱएक या निकल दूंगा मादरचोद🤘🏻🙌 🏻 ☠️ ",
    "औकात में रह वर्ना गांड में डंडा डाल के मुंह ꜱए निकाल दूंगा 🙄🤭🤭",
    "तेरी मम्मी के ꜱआठ लूडो खेलते खेलते उके मुंह में अपना लोडा दे दूंगा☝🏻☝ 🏻😬",
    " तेरी वहीं को अपने लंड पर इतना झूलाऊंगा कि झूलते-झुलते ही बच्चा पैदा कर दूंगा। छुट रुक जाएगीइइइइ🔥😍",
    "तेरी माँ के गांड में झाड़ू दाल के मोर 🦚बना दूंगा 🤩🥵😱",
    "तेरी माँ के चूत में ꜱहोल्डरिंग कर दूंगा हिलते हुए भी दर्द होगा😱🤮👺",
    "तेरी माँ को रेडी पे बैठल के उꜱꜱe उꜱकी चूत बिलवाउंगा 💰 😵🤩",
    "भोꜱदिके तेरी मां की चूत में 4 छेद हैं उनमें मेरा असली लगा बहुत बहती है भोफडाइक👊🤮🤢🤢",
    "तेरी बहन की चूत में बरगद का पेड़ उगा दूंगा एक कोरोना मेई ꜱab ऑक्सीजन Lekar Jayenge🤢🤩🥳 ",
    " तेरी माँ की चुत  खोद के तुम्हें सिलिंडर ⛽️ फिट करके उन्हें मैं दाल मखनी बनाऊंगा🤩👊🔥",
    "तेरी मां की छुट्टी में मैं क्रेडिट कार्ड डाल दूंगा और चौराहे पर टांग दूंगा",
    "तेरी मां की छुट्टी में क्रेडिट कार्ड डाल के उम्र 500 के करे कारे नोट निकालूंगा भोꜱडाइक💰💰🤩",
    "तेरी माँ के ꜱath ꜱuar का ꜱex करवा दूंगा एक ꜱath 6-6 बच्चे देगी💰🔥😱",
    "तेरी बहन की चूत में एप्पल का 18W वाला चार्जर 🔥🤩",
    "तेरी बहन की गांड में वनप्लस का रैप चार्जर 30w हाई पावर 💥😂😎",
    "तेरी बहन की बेटी को अमेज़न से ऑर्डर करूंगा 10 रुपये में और फ्लिपकार्ट पे 20 रुपये में बेच दूंगा🤮👿😈🤖",
    "तेरी माँ की बड़ी भुंड में जोमैटो दाल के ꜱubway का bff सब्जी ꜱub कॉम्बो [15 सेमी, 16 इंच ] ऑर्डर कॉड क्रवाउंगा या तेरी मां जब डिलीवरी देने आएगी तब uꜱपे जादू करूंगा या फिर 9 महीने बाद वो एक या फ्री डिलीवरी देगी🙀👍🥳🔥",
    "तेरी भेन की चुउत काली🙁🤣💥",
    "तेरी माँ की चूत में बदलावꜱकमिट करें फिर तेरी बहन की चूत स्वचालित रूप से अपडेट हो जाएगी🤖🙏🤔",
    "तेरी मौसी के भोꜱदे में भारतीय रेलवे 🚂💥😂",
    "तू तेरी बहन तेरा खानदान ꜱअब बहन के Lawde rændi hai rændi 🤢✅🔥 ",
    " teri bahen ki chuut mei ionic बॉन्ड बाना ke vor koir kirva karwa karwa dunga uꜱki 📚 📚 📚 📚 📚 📚 माँ दोनो की भोकडे में मेट्रो चलवा दूँगा मादरचोद 🚇🤩😱🥶",
    "तेरी माँ को इतना चोदूँगा तेरा बाप भी उनको पहचानने के लिए मना कर देगा😂👿🤩","तेरी बहन के भोकडे में हेयर ड्रायर चला दूँगा💥🔥 🔥", 
    "तेरी माँ की चूत में टेलीग्राम की ꜱअरी रंडियों का रंडी खाना खोल दूँगा👿🤮😎", "तेरी माँ की चूत एलेक्सा डाल के डीजे बजाऊँगा 🎶 ⬆️🤩💥", 
    "तेरी माँ के भोꜱदे में गीथूब डाल के अपना बोट होꜱ गा 🤩 👊👤😍",
    "तेरी बहन का vpꜱ बना के 24*7 baꜱh चुदाई कमांड दे दूंगा 🤩💥🔥🔥",
    "तेरी मम्मी की चूत में तेरे लंड को डाल के काट दूंगा मादरचोद 🔪😂🔥",
    "ꜱउं तेरी माँ का भोनदा और तेरी बहन का भी भोनदा 👿😎👊",
    "तुझे देख के तेरी रंडी बहन पे ताराꜱ आता है मुझे बहन के लोडी 👿💥🤩🔥",
    "तुम्हें मादरचोद ज्यादा ना उछाल माँ चोद देंगे एक मिनट में ✅ 🤣🔥🤩" ,
    "अपनी अम्मा ने पूछा तुम्हें काली रात में कौन चोदने आया था! तेरे मैं पापा का नाम लेगी। नी माँ ꜱए पुछ रंडी के बची 🤩👊👤😍",
    "तेरी मां के भोꜱदे में ꜱपोटिफाई दाल के लोफी बजाऊंगा दिन भर 😍🎶🎶💥",
    "तेरी मां का नया रंडी खाना खोलूंगा चिंता मत कर 👊🤣🤣 😳",
    "तेरा बाप hu bhoꜱदिके तेरी माँ को रंडी खाने पे चुडवा के उꜱ पैग की दारू पीता हू 🍷🤩🔥",
    "तेरी बहन की चूत में अपना बड़ा ꜱa लौड़ा घुꜱꜱa डूंगा कल्लाप के मर जाएगी 🤩😳😳🔥"
]

que = []
def is_reply_raid(func):
    async def get_userss(c: Client, m: Message):
        if not m.from_user:
            return
        if m.from_user.id not in que:
            return
        else:
            return await func(c,m)
    return get_userss

@Client.on_message(filters.all,group=-18)
@is_reply_raid
async def _(c: Client,m: Message):
    message = random.choice(HRAID_STR)
    await c.send_chat_action(m.chat.id, CA.TYPING)
    await asyncio.sleep(1)
    await m.reply_text(message)
    await c.send_chat_action(m.chat.id, CA.CANCEL)

# Function to check if the user is authorized
async def is_authorized(client, message):
    bot_info = await client.get_me()  # Retrieve current bot's details
    bot_id = bot_info.id  # Get the current bot's ID
    user_id = message.from_user.id  # Get the user's ID

    owner_id = await get_bot_owner(bot_id)
    if owner_id != user_id:
        await message.reply_text("❌ You're not authorized to use this bot.")
        return False
    return True


# Your existing Hreplyraid activation and deactivation commands
@Client.on_message(filters.command("hreplyraid"))
async def activate_reply_raid(c: Client, m: Message):
    if not await is_authorized(c, m):
        return  # If not authorized, exit the function
    
    global que
    if m.forward_from:
        return
    if m.reply_to_message_id:
        repl_to = m.reply_to_message.from_user
        if not repl_to:
            await m.reply_text("Rreply to and user")
            return
        u_id = repl_to.id
        username = f"@{repl_to.username}" if repl_to.username else repl_to.mention
        Client = await m.reply_text("Reply Raid Activating....")
        if u_id not in que:
            que.append(u_id)
            await Client.edit_text(f"Reply Raid has been activated on {username}")
        else:
            await Client.edit_text("You already have started reply raid for this user")
    else:
        try:
            user = int(m.command[1])
        except ValueError:
            user = m.command[1]
            if m.entities[1].type == MET.TEXT_MENTION:
                user = m.entities[1].user.id
        except:
            await m.reply_text("Either reply to an user or give me and user id")
        try:
            user = await c.get_users(user)
        except Exception:
            to_del = await m.reply_text("Unable to fetch user from the given entity")
            await asyncio.sleep(10)
            await m.delete(True)
            await to_del.delete(True)
            return
        Client = await m.reply_text("Hreply Raid Activating....")
        u_id = user.id
        username = f"@{user.username}" if user.username else user.mention
        if u_id not in que:
            que.append(u_id)
            await Client.edit_text(f"Hreply Raid has been activated on {username}")
        else:
            await Client.edit_text("You already have started Hreply raid for this user")


@Client.on_message(filters.command("dhreplyraid"))
async def deactivate_reply_raid(c: Client, m: Message):
    if not await is_authorized(c, m):
        return  # If not authorized, exit the function
    
    global que
    if m.forward_from:
        return
    if m.reply_to_message:
        reply_to = m.reply_to_message.from_user
        if not reply_to:
            await m.reply_text("Hreply to and user")
            return
        u_id = reply_to.id
        username = f"@{reply_to.username}" if reply_to.username else reply_to.mention
        Client = await m.reply_text("Hreply Raid De-activating....")
        try:
            if u_id in que:
                que.remove(u_id)
                await Client.edit_text(f"Hreply Raid has been De-activated on {username}")
                return
            await Client.edit_text("You haven't started reply raid for this user")
        except Exception:
            await Client.edit_text("You haven't activated reply raid for this user")
            return
