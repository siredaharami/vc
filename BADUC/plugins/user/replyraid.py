import random
import asyncio

from BADUC import SUDOERS
from BADUC.core.clients import app
from BADUC.core.command import *

from pyrogram import Client, filters
from pyrogram.enums import MessageEntityType as MET, ChatAction as CA
from pyrogram.types import Message


RAID_STR = [
    "MADARCHOD TERI MAA KI CHUT ME GHUTKA KHAAKE THOOK DUNGA 🤣🤣",
    "TERE BEHEN K CHUT ME CHAKU DAAL KAR CHUT KA KHOON KAR DUGA",
    "TERI VAHEEN NHI HAI KYA? 9 MAHINE RUK SAGI VAHEEN DETA HU 🤣🤣🤩",
    "TERI MAA K BHOSDE ME AEROPLANEPARK KARKE UDAAN BHAR DUGA ✈️🛫",
    "TERI MAA KI CHUT ME SUTLI BOMB FOD DUNGA TERI MAA KI JHAATE JAL KE KHAAK HO JAYEGI💣",
    "TERI MAAKI CHUT ME SCOOTER DAAL DUGA👅",
    "TERE BEHEN K CHUT ME CHAKU DAAL KAR CHUT KA KHOON KAR DUGA",
    "TERE BEHEN K CHUT ME CHAKU DAAL KAR CHUT KA KHOON KAR DUGA",
    "TERI MAA KI CHUT KAKTE 🤱 GALI KE KUTTO 🦮 ME BAAT DUNGA PHIR 🍞 BREAD KI TARH KHAYENGE WO TERI MAA KI CHUT",
    "DUDH HILAAUNGA TERI VAHEEN KE UPR NICHE 🆙🆒😙",
    "TERI MAA KI CHUT ME ✋ HATTH DALKE 👶 BACCHE NIKAL DUNGA 😍",
    "TERI BEHN KI CHUT ME KELE KE CHILKE 🍌🍌😍",
    "TERI BHEN KI CHUT ME USERBOT LAGAAUNGA SASTE SPAM KE CHODE",
    "TERI VAHEEN DHANDHE VAALI 😋😛",
    "TERI MAA KE BHOSDE ME AC LAGA DUNGA SAARI GARMI NIKAL JAAYEGI",
    "TERI VAHEEN KO HORLICKS PEELAUNGA MADARCHOD😚",
    "TERI MAA KI GAAND ME SARIYA DAAL DUNGA MADARCHOD USI SARIYE PR TANG KE BACHE PAIDA HONGE 😱😱",
    "TERI MAA KO KOLKATA VAALE JITU BHAIYA KA LUND MUBARAK 🤩🤩",
    "TERI MUMMY KI FANTASY HU LAWDE, TU APNI BHEN KO SMBHAAL 😈😈",
    "TERA PEHLA BAAP HU MADARCHOD ",
    "TERI VAHEEN KE BHOSDE ME XVIDEOS.COM CHALA KE MUTH MAARUNGA 🤡😹",
    "TERI MAA KA GROUP VAALON SAATH MILKE GANG BANG KRUNGA🙌🏻☠️ ",
    "TERI ITEM KI GAAND ME LUND DAALKE,TERE JAISA EK OR NIKAAL DUNGA MADARCHOD🤘🏻🙌🏻☠️ ",
    "AUKAAT ME REH VRNA GAAND ME DANDA DAAL KE MUH SE NIKAAL DUNGA SHARIR BHI DANDE JESA DIKHEGA 🙄🤭🤭",
    "TERI MUMMY KE SAATH LUDO KHELTE KHELTE USKE MUH ME APNA LODA DE DUNGA☝🏻☝🏻😬",
    "TERI VAHEEN KO APNE LUND PR ITNA JHULAAUNGA KI JHULTE JHULTE HI BACHA PAIDA KR DEGI👀👯 ",
    "TERI MAA KI CHUT MEI BATTERY LAGA KE POWERBANK BANA DUNGA 🔋 🔥🤩",
    "TERI MAA KI CHUT MEI C++ STRING ENCRYPTION LAGA DUNGA BAHTI HUYI CHUT RUK JAYEGIIII😈🔥😍",
    "TERI MAA KE GAAND MEI JHAADU DAL KE MOR 🦚 BANA DUNGAA 🤩🥵😱",
    "TERI CHUT KI CHUT MEI SHOULDERING KAR DUNGAA HILATE HUYE BHI DARD HOGAAA😱🤮👺",
    "TERI MAA KO REDI PE BAITHAL KE USSE USKI CHUT BILWAUNGAA 💰 😵🤩",
    "BHOSDIKE TERI MAA KI CHUT MEI 4 HOLE HAI UNME MSEAL LAGA BAHUT BAHETI HAI BHOFDIKE👊🤮🤢🤢",
    "TERI BAHEN KI CHUT MEI BARGAD KA PED UGA DUNGAA CORONA MEI SAB OXYGEN LEKAR JAYENGE🤢🤩🥳",
    "TERI MAA KI CHUT MEI SUDO LAGA KE BIGSPAM LAGA KE 9999 FUCK LAGAA DU 🤩🥳🔥",
    "TERI VAHEN KE BHOSDIKE MEI BESAN KE LADDU BHAR DUNGA🤩🥳🔥😈",
    "TERI MAA KI CHUT KHOD KE USME CYLINDER ⛽️ FIT KARKE USMEE DAL MAKHANI BANAUNGAAA🤩👊🔥",
    "TERI MAA KI CHUT MEI SHEESHA DAL DUNGAAA AUR CHAURAHE PE TAANG DUNGA BHOSDIKE😈😱🤩",
    "TERI MAA KI CHUT MEI CREDIT CARD DAL KE AGE SE 500 KE KAARE KAARE NOTE NIKALUNGAA BHOSDIKE💰💰🤩",
    "TERI MAA KE SATH SUAR KA SEX KARWA DUNGAA EK SATH 6-6 BACHE DEGI💰🔥😱",
    "TERI BAHEN KI CHUT MEI APPLE KA 18W WALA CHARGER 🔥🤩",
    "TERI BAHEN KI GAAND MEI ONEPLUS KA WRAP CHARGER 30W HIGH POWER 💥😂😎",
    "TERI BAHEN KI CHUT KO AMAZON SE ORDER KARUNGA 10 rs MEI AUR FLIPKART PE 20 RS MEI BECH DUNGA🤮👿😈🤖",
    "TERI MAA KI BADI BHUND ME ZOMATO DAL KE SUBWAY KA BFF VEG SUB COMBO [15cm , 16 inches ] ORDER COD KRVAUNGA OR TERI MAA JAB DILIVERY DENE AYEGI TAB USPE JAADU KRUNGA OR FIR 9 MONTH BAAD VO EK OR FREE DILIVERY DEGI🙀👍🥳🔥",
    "TERI BHEN KI CHUT KAALI🙁🤣💥",
    "TERI MAA KI CHUT ME CHANGES COMMIT KRUGA FIR TERI BHEEN KI CHUT AUTOMATICALLY UPDATE HOJAAYEGI🤖🙏🤔",
    "TERI MAUSI KE BHOSDE MEI INDIAN RAILWAY 🚂💥😂",
    "TU TERI BAHEN TERA KHANDAN SAB BAHEN KE LAWDE RANDI HAI RANDI 🤢✅🔥",
    "TERI BAHEN KI CHUT MEI IONIC BOND BANA KE VIRGINITY LOOSE KARWA DUNGA USKI 📚 😎🤩",
    "TERI RANDI MAA SE PUCHNA BAAP KA NAAM BAHEN KE LODEEEEE 🤩🥳😳",
    "TU AUR TERI MAA DONO KI BHOSDE MEI METRO CHALWA DUNGA MADARXHOD 🚇🤩😱🥶",
    "TERI MAA KO ITNA CHODUNGA TERA BAAP BHI USKO PAHCHANANE SE MANA KAR DEGA😂👿🤩",
    "TERI BAHEN KE BHOSDE MEI HAIR DRYER CHALA DUNGAA💥🔥🔥",
    "TERI MAA KI CHUT MEI TELEGRAM KI SARI RANDIYON KA RANDI KHANA KHOL DUNGAA👿🤮😎",
    "TERI MAA KI CHUT ALEXA DAL KEE DJ BAJAUNGAAA 🎶 ⬆️🤩💥",
    "TERI MAA KE BHOSDE MEI GITHUB DAL KE APNA BOT HOST KARUNGAA 🤩👊👤😍",
    "TERI BAHEN KA VPS BANA KE 24*7 BASH CHUDAI COMMAND DE DUNGAA 🤩💥🔥🔥",
    "TERI MUMMY KI CHUT MEI TERE LAND KO DAL KE KAAT DUNGA MADARCHOD 🔪😂🔥",
    "SUN TERI MAA KA BHOSDA AUR TERI BAHEN KA BHI BHOSDA 👿😎👊",
    "TUJHE DEKH KE TERI RANDI BAHEN PE TARAS ATA HAI MUJHE BAHEN KE LODEEEE 👿💥🤩🔥",
    "SUN MADARCHOD JYADA NA UCHAL MAA CHOD DENGE EK MIN MEI ✅🤣🔥🤩",
    "APNI AMMA SE PUCHNA USKO US KAALI RAAT MEI KAUN CHODNEE AYA THAAA! TERE IS PAPA KA NAAM LEGI 😂👿😳",
    "TOHAR BAHIN CHODU BBAHEN KE LAWDE USME MITTI DAL KE CEMENT SE BHAR DU 🏠🤢🤩💥",
    "TUJHE AB TAK NAHI SMJH AYA KI MAI HI HU TUJHE PAIDA KARNE WALA BHOSDIKEE APNI MAA SE PUCH RANDI KE BACHEEEE 🤩👊👤😍",
    "TERI MAA KE BHOSDE MEI SPOTIFY DAL KE LOFI BAJAUNGA DIN BHAR 😍🎶🎶💥",
    "TERI MAA KA NAYA RANDI KHANA KHOLUNGA CHINTA MAT KAR 👊🤣🤣😳",
    "TERA BAAP HU BHOSDIKE TERI MAA KO RANDI KHANE PE CHUDWA KE US PAISE KI DAARU PEETA HU 🍷🤩🔥",
    "TERI BAHEN KI CHUT MEI APNA BADA SA LODA GHUSSA DUNGAA KALLAAP KE MAR JAYEGI 🤩😳😳🔥",
    "TOHAR MUMMY KI CHUT MEI PURI KI PURI KINGFISHER KI BOTTLE DAL KE TOD DUNGA ANDER HI 😱😂🤩",
    "TERI MAA KO ITNA CHODUNGA KI SAPNE MEI BHI MERI CHUDAI YAAD KAREGI RANDI 🥳😍👊💥",
    "TERI MUMMY AUR BAHEN KO DAUDA DAUDA NE CHODUNGA UNKE NO BOLNE PE BHI LAND GHUSA DUNGA ANDER TAK 😎😎🤣🔥",
    "TERI MUMMY KI CHUT KO ONLINE OLX PE BECHUNGA AUR PAISE SE TERI BAHEN KA KOTHA KHOL DUNGA 😎🤩😝😍",
    "TERI MAA KE BHOSDA ITNA CHODUNGA KI TU CAH KE BHI WO MAST CHUDAI SE DUR NHI JA PAYEGAA 😏😏🤩😍",
    "SUN BE RANDI KI AULAAD TU APNI BAHEN SE SEEKH KUCH KAISE GAAND MARWATE HAI😏🤬🔥💥",
    "TERI MAA KA YAAR HU MEI AUR TERI BAHEN KA PYAAR HU MEI AJA MERA LAND CHOOS LE 🤩🤣💥",
    "MADARCHOD",
    "BHOSDIKE",
    "LAAAWEEE KE BAAAAAL",
    "MAAAAR KI JHAAAAT KE BBBBBAAAAALLLLL",
    "MADRCHOD..",
    "TERI MA KI CHUT..",
    "LWDE KE BAAALLL.",
    "MACHAR KI JHAAT KE BAAALLLL",
    "TERI MA KI CHUT M DU TAPA TAP?",
    "TERI MA KA BHOSDAA",
    "TERI BHN SBSBE BDI RANDI.",
    "TERI MA OSSE BADI RANDDDDD",
    "TERA BAAP CHKAAAA",
    "KITNI CHODU TERI MA AB OR..",
    "TERI MA CHOD DI HM NE",
    "TERI MA KE STH REELS BNEGA ROAD PEE",
    "TERI MA KI CHUT EK DAM TOP SEXY",
    "MALUM NA PHR KESE LETA HU M TERI MA KI CHUT TAPA TAPPPPP",
    "LUND KE CHODE TU KEREGA TYPIN",
    "SPEED PKD LWDEEEE",
    "BAAP KI SPEED MTCH KRRR",
    "LWDEEE",
    "PAPA KI SPEED MTCH NHI HO RHI KYA",
    "ALE ALE MELA BCHAAAA",
    "CHUD GYA PAPA SEEE",
    "KISAN KO KHODNA OR",
    "SALE RAPEKL KRDKA TERA",
    "HAHAHAAAAA",
    "KIDSSSS",
    "TERI MA CHUD GYI AB FRAR MT HONA",
    "YE LDNGE BAPP SE",
    "KIDSSS FRAR HAHAHH",
    "BHEN KE LWDE SHRM KR",
    "KITNI GLIYA PDWEGA APNI MA KO",
    "NALLEE",
    "SHRM KR",
    "MERE LUND KE BAAAAALLLLL",
    "KITNI GLIYA PDWYGA APNI MA BHEN KO",
    "RNDI KE LDKEEEEEEEEE",
    "KIDSSSSSSSSSSSS",
    "Apni gaand mein muthi daal",
    "Apni lund choos",
    "Apni ma ko ja choos",
    "Bhen ke laude",
    "Bhen ke takke",
    "Abla TERA KHAN DAN CHODNE KI BARIII",
    "BETE TERI MA SBSE BDI RAND",
    "LUND KE BAAAL JHAT KE PISSSUUUUUUU",
    "LUND PE LTKIT MAAALLLL KI BOND H TUUU",
    "KASH OS DIN MUTH MRKE SOJTA M TUN PAIDA NA HOTAA",
    "GLTI KRDI TUJW PAIDA KRKE",
    "SPEED PKDDD",
    "Gaand main LWDA DAL LE APNI MERAAA",
    "Gaand mein bambu DEDUNGAAAAAA",
    "GAND FTI KE BALKKK",
    "Gote kitne bhi bade ho, lund ke niche hi rehte hai",
    "Hazaar lund teri gaand main",
    "Jhaant ke pissu-",
    "TERI MA KI KALI CHUT",
    "Khotey ki aulda",
    "Kutte ka awlat",
    "Kutte ki jat",
    "Kutte ke tatte",
    "TETI MA KI.CHUT , tERI MA RNDIIIIIIIIIIIIIIIIIIII",
    "Lavde ke bal",
    "muh mei lele",
    "Lund Ke Pasine",
    "MERE LWDE KE BAAAAALLL",
    "HAHAHAAAAAA",
    "CHUD GYAAAAA",
    "Randi khanE KI ULADDD",
    "Sadi hui gaand",
    "Teri gaand main kute ka lund",
    "Teri maa ka bhosda",
    "Teri maa ki chut",
    "Tere gaand mein keede paday",
    "Ullu ke pathe",
    "SUNN MADERCHOD",
    "TERI MAA KA BHOSDA",
    "BEHEN K LUND",
    "TERI MAA KA CHUT KI CHTNIIII",
    "MERA LAWDA LELE TU AGAR CHAIYE TOH",
    "GAANDU",
    "CHUTIYA",
    "TERI MAA KI CHUT PE JCB CHADHAA DUNGA",
    "SAMJHAA LAWDE",
    "YA DU TERE GAAND ME TAPAA TAP��",
    "TERI BEHEN MERA ROZ LETI HAI",
    "TERI GF K SAATH MMS BANAA CHUKA HU���不�不",
    "TU CHUTIYA TERA KHANDAAN CHUTIYA",
    "AUR KITNA BOLU BEY MANN BHAR GAYA MERA�不",
    "TERIIIIII MAAAA KI CHUTTT ME ABCD LIKH DUNGA MAA KE LODE",
    "TERI MAA KO LEKAR MAI FARAR",
    "RANIDIII",
    "BACHEE",
    "CHODU",
    "RANDI",
    "RANDI KE PILLE",
    "TERIIIII MAAA KO BHEJJJ",
    "TERAA BAAAAP HU",
    "teri MAA KI CHUT ME HAAT DAALLKE BHAAG JAANUGA",
    "Teri maa KO SARAK PE LETAA DUNGA",
    "TERI MAA KO GB ROAD PE LEJAKE BECH DUNGA",
    "Teri maa KI CHUT MÉ KAALI MITCH",
    "TERI MAA SASTI RANDI HAI",
    "TERI MAA KI CHUT ME KABUTAR DAAL KE SOUP BANAUNGA MADARCHOD",
    "TERI MAAA RANDI HAI",
    "TERI MAAA KI CHUT ME DETOL DAAL DUNGA MADARCHOD",
    "TERI MAA KAAA BHOSDAA",
    "TERI MAA KI CHUT ME LAPTOP",
    "Teri maa RANDI HAI",
    "TERI MAA KO BISTAR PE LETAAKE CHODUNGA",
    "TERI MAA KO AMERICA GHUMAAUNGA MADARCHOD",
    "TERI MAA KI CHUT ME NAARIYAL PHOR DUNGA",
    "TERI MAA KE GAND ME DETOL DAAL DUNGA",
    "TERI MAAA KO HORLICKS PILAUNGA MADARCHOD",
    "TERI MAA KO SARAK PE LETAAA DUNGAAA",
    "TERI MAA KAA BHOSDA",
    "MERAAA LUND PAKAD LE MADARCHOD",
    "CHUP TERI MAA AKAA BHOSDAA",
    "TERIII MAA CHUF GEYII KYAAA LAWDEEE",
    "TERIII MAA KAA BJSODAAA",
    "MADARXHODDD",
    "TERIUUI MAAA KAA BHSODAAA",
    "TERIIIIII BEHENNNN KO CHODDDUUUU MADARXHODDDD",
    "NIKAL MADARCHOD",
    "RANDI KE BACHE",
    "TERA MAA MERI FAN",
    "TERI SEXY BAHEN KI CHUT OP",
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

@app.on_message(filters.all,group=-18)
@is_reply_raid
async def _(c: Client,m: Message):
    message = random.choice(RAID_STR)
    await c.send_chat_action(m.chat.id, CA.TYPING)
    await asyncio.sleep(1)
    await m.reply_text(message)
    await c.send_chat_action(m.chat.id, CA.CANCEL)

@app.on_message(bad(["replyraid"]) & (filters.me | filters.user(SUDOERS)))
async def activate_reply_raid(c: Client,m: Message):
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
        app = await m.reply_text("Reply Raid Activating....")
        if u_id not in que:
            que.append(u_id)
            await app.edit_text(f"Reply Raid has been activated on {username}")
        else:
            await app.edit_text("You already have started reply raid for this user")
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
        app = await m.reply_text("Reply Raid Activating....")
        u_id = user.id
        username = f"@{user.username}" if user.username else user.mention
        if u_id not in que:
            que.append(u_id)
            await app.edit_text(f"Reply Raid has been activated on {username}")
        else:
            await app.edit_text("You already have started reply raid for this user")


@app.on_message(bad(["dreplyraid"]) & (filters.me | filters.user(SUDOERS)))
async def deactivate_reply_raid(c: Client, m: Message):
    global que
    if m.forward_from:
        return
    if m.reply_to_message:
        reply_to = m.reply_to_message.from_user
        if not reply_to:
            await m.reply_text("Rreply to and user")
            return
        u_id = reply_to.id
        username = f"@{reply_to.username}" if reply_to.username else reply_to.mention
        app = await m.reply_text("Reply Raid De-activating....")
        try:
            if u_id in que:
                que.remove(u_id)
                await app.edit_text(f"Reply Raid has been De-activated on {username}")
                return
            await app.edit_text("You haven't started reply raid for this user")
        except Exception:
            await app.edit_text("You haven't activated reply raid for this user")
            return
        
    else:
        try:
            user = int(m.command[1])
        except ValueError:
            user = m.command[1]
            if m.entities[1].type == MET.TEXT_MENTION:
                user = m.entities[1].user.id
        try:
            user = await c.get_users(user)
        except Exception:
            to_del = await m.reply_text("Unable to fetch user from the given entity")
            await asyncio.sleep(10)
            await m.delete(True)
            await to_del.delete(True)
            return
        app = await m.reply_text("Reply Raid De-activating....")
        u_id = user.id
        username = f"@{user.username}" if user.username else user.mention
        try:
            if u_id in que:
                que.remove(u_id)
                await app.edit_text(f"Reply Raid has been De-activated on {username}")
                return
            await app.edit_text("You haven't started reply raid for this user")
        except Exception:
            await app.edit_text("You haven't activated reply raid for this user")
            return
              

#PBIREPLYRAID

PRAID_STR = [
   "🥹ਬਾਰੀ ਬਰਸੀ ਖੱਟਣ ਗਿਆ ਸੀ ਖੱਟ ਕੇ ਲਿਆਂਦਾ ਬੱਲਾ ਤੇਰੀ ਭੈਣ ਦਾ ਫੁੱਦਾ ਮਾਰੇ ਗਰੁੱਪ ਦਾ ਮੇਂਬਰ ਕੱਲਾ ਕੱਲਾ😭",
"😈ਬਾਰੀ ਬਰਸੀ ਖੱਟਣ ਗਿਆ ਸੀ ਖੱਟ ਕੇ ਲਿਆਂਦਾ ਆਲੂ ਪਿਓ ਤੇਰਾ ਟੈਮਪੂ ਮਾਂ ਤੇਰੀ ਚਾਲੂ😈",
"🥵ਬਾਰੀ ਬਰਸੀ ਖੱਟਣ ਗਿਆ ਸੀ ਖੱਟ ਕੇ ਲਿਆਂਦਾ ਫੂਸਾ ਮੇਰਾ ਡੈਡੀ ਤੇਰੀ ਬੁੰਡ ਮਾਰੇ ਮੈ ਮਾਰਾਂ ਤੇਰੀ ਭੈਣ ਦਾ ਘੁਸਾ👅",
"🥵ਵਾਰੀ ਵਰਸੀ ਖੱਟਣ ਗਿਆ ਸੀ ਖੱਟ ਕੇ ਲਿਆਂਦਾ ਸ਼ੇਮਪੂ ਮਾਂ ਤੇ bhen ਤੇਰੀ ਸਿੱਰੇ ਦੀ ਟੈਕਸੀ ਤੂੰ ਤੇ ਤੇਰਾ ਪਿਓ ਪਿੰਡ ਦੇ ਮਸ਼ਹੂਰ ਟੈਮਪੂ👅",
"😈ਵਾਰੀ ਵਰਸੀ ਖੱਟਣ ਗਿਆ ਸੀ ਖੱਟ ਕੇ ਲਿਆਂਦਾ ਵੱਟਾ ਮਾਂ ਤੇ ਤੇਰੀ ਭੈਣ ਦੇ ਲੁੱਲਾ ਪਾਵਾ ਤੇਰਾ ਪਿਓ ਥੱਲੋ ਦੀ ਚੁੰਗੇ ਮੇਰਾ ਟੱਟਆ👅",
"🥺ਵਾਰੀ ਵਰਸੀ ਖੱਟਣ ਗਿਆ ਸੀ ਖੱਟ ਕੇ ਲਿਆਂਦਾ ਅੰਬਾ ਤੇਰੀ ਮਾਂ ਦੇ ਸ਼ੋਲ਼ੇ ਚ ਮਾਰਾਂ 90 ਗਜ ਦਾ ਟੰਬਾ😭",
"🥹ਬਾਰੀ ਬਰਸੀ ਖੱਟਣ ਗਿਆ ਸੀ ਖੱਟ ਕੇ ਲਿਆਂਦਾ ਟੰਬਾ ਤੇਰੀ ਮਾਂ ਤੇ ਚੜਜੇ ਮੇਰਾ ਪਿਓ ਤੇ me ਤੇਰੀ ਬੁੰਡ ਚ ਮਾਰਾਂ ਖਮਬਾ😈",
"😭ਬਾਰੀ ਬਰਸੀ ਖੱਟਣ ਗਿਆ ਸੀ ਖੱਟ ਕੇ ਲਿਆਂਦਾ ਫੇਬੂ ਤੇਰੀ ਮਾਂ ਦਾ ਫੁੱਦੜਾ ਮਾਰੇ ਸਾਡੇ ਪਿੰਡ ਵਾਲਾ ਬਿੱਕਰ ਸੇਬੂ🥵",
"👅ਬੜੀ ਬਰਸੀ ਖੱਟਣ ਗਿਆ ਸੀ ਖੱਟ ਕੇ ਲਿਆਂਦੀ ਲਾਲੀ ਤੇਰੇ ਪਿਓ ਦੇ ਮਾਰਾਂ ਲੁੱਲਾ ਤੇਰੀ ਭੈਣ ਦੇ ਸ਼ੋਲ਼ੇ ਚ ਟਰਾਲ਼ੀ👅",
"🥵ਬਾਰੀ ਬਰਸੀ ਖੱਟਣ ਗਏ ਸੀ ਖੱਟ ਕੇ ਲਿਆਂਦਾ ਬੈਡ ਤੇਰੀ ਮਾਂ ਤੇ ਤੇਰੇ ਪਿਓ ਦੀ ਪੱਟਾਂ ਬੁੰਡ ਤੇਰੀ ਭੈਣ ਦੇ ਫੁੜਦੇ ਚ ਸ਼ੈੱਡ😭",
"🥹ਬਾਰੀ ਬਰਸੀ ਖੱਟਣ ਗਿਆ ਸੀ ਖੱਟ ਕੇ ਲਿਆਂਦੀ ਰੀਡ ਆਵਦੀ ਮਾਂ ਤੇ ਭਵਨ ਕਰ ਨੰਗੀ ਜੇ ਮੈਚ ਨੀ ਹੁੰਦੀ ਸਪੀਡ🥹",
"🥵ਕਹਿੰਦੇ ਆਰ ਟਾਂਗਾ ਪਾਰ ਟਾਂਗਾ ਵਿਚ ਟਾਂਗਾ ਦੇ ਟੋਏ ਤੇਰੀ ਭੈਣ ਦਾ ਫੁੱਦਾ ਮਾਰਾਂ ਤੇਰਾ ਪਿਓ ਕੋਲ ਖੜਾ ਕਰੇ ਓਏ ਓਏ🥹"
"👅ਕਹਿੰਦੇ ਆਰ ਟਾਂਗਾ ਪਾਰ ਟਾਂਗਾ ਵਿਚ ਟਾਂਗਾ ਦੇ ਹੁਲ ਤੇਰੀ ਮਾਂ ਦੀ ਮਾਰਾਂ ਸ਼ੋਲੀ ਤੇਰੀ ਭੈਣ ਦੇ ਫੁੜਦੇ ਚ 10 ਗਜ ਦਾ ਲੁੱਲ🥵",
"😭ਬਾਰੀ ਬਰਸੀ ਖੱਟਣ ਗਿਆ ਸੀ ਖੱਟ ਕੇ ਲਿਆਂਦੀ ਤੋਰੀ ਪਿਓ ਤੇਰਾ ਸ਼ੱਕਾ ਤੇਰੀ ਮਾਂ ਦੀ ਫੁੱਦੀ ਚ ਬਹੁਤ ਵੱਡੀ ਮੋਰੀ😭",
"🥵ਬਾਰੀ ਬਰਸੀ ਖੱਟਣ ਗਿਆ ਸੀ ਖੱਟ ਕੇ ਲਿਆਂਦਾ ਕੱਮ ਤੇਰਾ ਪਿਓ ਲਾਵੇ ਚੁੱਪੇ ਤੇਰੀ ਭੈਣ ਦੇ ਫੁੜਦੇ ਚ ਡਰੱਮ👅",
"ਕੱਚ ਦੀ ਗਲਾਸੀ ਵਿਚ ਬੂਟਾ ਭੰਗ ਦਾ ਇੱਕ ਵਾਰ ਦੇਦੇ ਫੇਰ ਨੀ ਮੰਗਦਾ",
"ਕੱਚ ਦੇ ਗਲਸ ਵਿਚ 🥵👅 ਤੋਤਾ ਬੋਲਦਾ 🥵👅ਤੇਰੇ ਵਰਗੇ ਦੀ ਮੈ ਤੁਰੇ ਜਾਂਦੇ 🥵👅",
"ਵਾਰ ੀ ਵਰਸੀ ਖੱਟਣ ਗਿਆ ਸੀ 🥵👅 ਖੱਟ ਕੇ ਲਿਆਂਦਾ ਪੋਲਾ 🥵👅 ਤੇਰੀ ਭੈਣ ਦੀ ਫੁੱਦੀ 🥵👅 ਤੇਰੀ ਮਾਂ ਦਾ ਪਾਟਿਆ ਸ਼ੋਲਾ 🥵👅",
"ਜੱਟ ਬੈਠਾ ਛਾਵੇ ਤੂਤ ਤੇਰੀ ਭੈਣ ਦੀ ਭੋਸੜੀ ਵਿਚ ਦੇਵਾ ਮੂਤ ",
"ਜੱਟ ਕਰਦਾ ਹੁਣ ਕੰਮ੍ਰ  ਜਾ ਸਾਲਿਆ ਆਪਣੀ ਭੈਣ ਦੀ ਭੋਸੜੀ ਦਾ ਨਾਲਾ ਜਾ ਕੇ ਬੰਨ",
"ਜੱਟ ਖੜਾ ਕੋਲ ਨਹਿਰ ਏ  ਪਹਿਲੇ ਪਹਿਰ ਚੜਿਆ ਤੇਰੀ ਭੈਣ ਤੇ ਉੱਤਰਿਆ ਚੌਥੇ ਪਹਿਰ ਏ",
"ਜੱਟ ਦੀ ਪੂਰੀ ਸਿਰੇ ਦੀ ਟੀਮ  ਤੇਰੀ ਬੁੰਡ ਚ ਪਾਉਣਾ ਸੱਤ ਫੁੱਟ ਸਰਿਆ ਦਾ ਵੀਮ",  
"ਕੇਹਂਦਾ ਬਾਰੀ ਬਰਸੀ ਖਟਨ ਗਿਆ ਖਟ ਕੇ ਲਿਆਂਦਾ ਕਲਿਪ ਫੁਦੀ ਵਿਚ ਲਨ ਵੜ ਗਿਆ ਟਟੇ ਮਾਰਨ ਸਲਿਪ",
"ਕੇਹਂਦਾ ਬਾਰੀ ਬਰਸੀ ਖਟਨ ਗਯਾ ਸੀ ਖੱਟ ਕੇ ਲਿਆਂਦੀ ਸ਼ੇਨੀ ਮੇਰੀ ਭਾਵੇਂ ਲਤ ਟੁੱਟ ਜਾਏ ਪਰਤੇਰੀ ਮੰਮੀ  ਦੀ ਫੁਦੀ ਕੰਦ ਓਥੇ ਭਠਾ ਕੇ ਲੈਣੀ 👅👅",
"ਕਹਿੰਦੇ ਤਾਰਾ ਤਾਰਾ ਤੇਰੀ ਭੇਣ ਦੀ ਚਕ ਕੇ ਲਤ ਬੁੰਡ ਮਾਰਾ👅👅👅",
"ਕੇਹਂਦਾ ਗਹਾਰਾ  ਗਹਾਰਾ ਮੁੜਕੇ ਤੂੰ ਇਹ ਗਰੁੱਪ ਚ ਨਹੁ ਦਿਖਣਾ ਜਦੋਂ ਲਨ ਚਕ ਤਾਂ ਤੇਰੇ  ਸਾਰਾ",
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

@app.on_message(filters.all,group=-18)
@is_reply_raid
async def _(c: Client,m: Message):
    message = random.choice(PRAID_STR)
    await c.send_chat_action(m.chat.id, CA.TYPING)
    await asyncio.sleep(1)
    await m.reply_text(message)
    await c.send_chat_action(m.chat.id, CA.CANCEL)

@app.on_message(bad(["preplyraid"]) & (filters.me | filters.user(SUDOERS)))
async def activate_reply_raid(c: Client,m: Message):
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
        app = await m.reply_text("Reply Raid Activating....")
        if u_id not in que:
            que.append(u_id)
            await app.edit_text(f"Reply Raid has been activated on {username}")
        else:
            await app.edit_text("You already have started reply raid for this user")
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
        app = await m.reply_text("Reply Raid Activating....")
        u_id = user.id
        username = f"@{user.username}" if user.username else user.mention
        if u_id not in que:
            que.append(u_id)
            await app.edit_text(f"Preply Raid has been activated on {username}")
        else:
            await app.edit_text("You already have started Preply raid for this user")


@app.on_message(bad(["dpreplyraid"]) & (filters.me | filters.user(SUDOERS)))
async def deactivate_reply_raid(c: Client, m: Message):
    global que
    if m.forward_from:
        return
    if m.reply_to_message:
        reply_to = m.reply_to_message.from_user
        if not reply_to:
            await m.reply_text("reply to and user")
            return
        u_id = reply_to.id
        username = f"@{reply_to.username}" if reply_to.username else reply_to.mention
        app = await m.reply_text("Preply Raid De-activating....")
        try:
            if u_id in que:
                que.remove(u_id)
                await app.edit_text(f"Preply Raid has been De-activated on {username}")
                return
            await app.edit_text("You haven't started reply raid for this user")
        except Exception:
            await app.edit_text("You haven't activated reply raid for this user")
            return
        
    else:
        try:
            user = int(m.command[1])
        except ValueError:
            user = m.command[1]
            if m.entities[1].type == MET.TEXT_MENTION:
                user = m.entities[1].user.id
        try:
            user = await c.get_users(user)
        except Exception:
            to_del = await m.reply_text("Unable to fetch user from the given entity")
            await asyncio.sleep(10)
            await m.delete(True)
            await to_del.delete(True)
            return
        app = await m.reply_text("Preply Raid De-activating....")
        u_id = user.id
        username = f"@{user.username}" if user.username else user.mention
        try:
            if u_id in que:
                que.remove(u_id)
                await app.edit_text(f"Preply Raid has been De-activated on {username}")
                return
            await app.edit_text("You haven't started reply raid for this user")
        except Exception:
            await app.edit_text("You haven't activated reply raid for this user")
            return
            
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

@app.on_message(filters.all,group=-18)
@is_reply_raid
async def _(c: Client,m: Message):
    message = random.choice(HRAID_STR)
    await c.send_chat_action(m.chat.id, CA.TYPING)
    await asyncio.sleep(1)
    await m.reply_text(message)
    await c.send_chat_action(m.chat.id, CA.CANCEL)

@app.on_message(bad(["hreplyraid"]) & (filters.me | filters.user(SUDOERS)))
async def activate_reply_raid(c: Client,m: Message):
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
        app = await m.reply_text("Reply Raid Activating....")
        if u_id not in que:
            que.append(u_id)
            await app.edit_text(f"Reply Raid has been activated on {username}")
        else:
            await app.edit_text("You already have started reply raid for this user")
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
        app = await m.reply_text("Hreply Raid Activating....")
        u_id = user.id
        username = f"@{user.username}" if user.username else user.mention
        if u_id not in que:
            que.append(u_id)
            await app.edit_text(f"Hreply Raid has been activated on {username}")
        else:
            await app.edit_text("You already have started Hreply raid for this user")


@app.on_message(bad(["dhreplyraid"]) & (filters.me | filters.user(SUDOERS)))
async def deactivate_reply_raid(c: Client, m: Message):
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
        app = await m.reply_text("Hreply Raid De-activating....")
        try:
            if u_id in que:
                que.remove(u_id)
                await app.edit_text(f"Hreply Raid has been De-activated on {username}")
                return
            await app.edit_text("You haven't started reply raid for this user")
        except Exception:
            await app.edit_text("You haven't activated reply raid for this user")
            return
        
    else:
        try:
            user = int(m.command[1])
        except ValueError:
            user = m.command[1]
            if m.entities[1].type == MET.TEXT_MENTION:
                user = m.entities[1].user.id
        try:
            user = await c.get_users(user)
        except Exception:
            to_del = await m.reply_text("Unable to fetch user from the given entity")
            await asyncio.sleep(10)
            await m.delete(True)
            await to_del.delete(True)
            return
        app = await m.reply_text("Hreply Raid De-activating....")
        u_id = user.id
        username = f"@{user.username}" if user.username else user.mention
        try:
            if u_id in que:
                que.remove(u_id)
                await app.edit_text(f"Hreply Raid has been De-activated on {username}")
                return
            await app.edit_text("You haven't started reply raid for this user")
        except Exception:
            await app.edit_text("You haven't activated reply raid for this user")
            return
            
