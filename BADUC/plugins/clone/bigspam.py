from BADUC import SUDOERS
from BADUC.core.command import *

from pyrogram import Client
from pyrogram.types import Message
from pyrogram.enums import ChatAction
from pyrogram import Client, filters

from asyncio import sleep

x = True

@Client.on_message(bad(["stopbigspam"]) & (filters.me | filters.user(SUDOERS)))
async def stopbigspam(c: Client, m: Message):
    await c.send_chat_action(m.chat.id, ChatAction.CANCEL)
    await m.reply_text("Stopped big spam")
    global x
    x = False



@Client.on_message(bad(["bigspam"]) & (filters.me | filters.user(SUDOERS)))
async def start_big_spam(c: Client, m: Message):
    xn = await m.reply_text("Startting galispam")
    await sleep(0.4)
    await xn.delete()
    await c.send_chat_action(m.chat.id,ChatAction.TYPING)
    while x == True:
        await m.delete()
        chat = m.chat.id
        await Client.send_message(chat, "SHURU")
        await Client.send_message(chat, "KARU")
        await Client.send_message(chat, "TERI XHUDAI")
        await Client.send_message(chat, "TERIII")
        await Client.send_message(chat, "MA")
        await Client.send_message(chat, "KI")
        await Client.send_message(chat, "XHUT")
        await Client.send_message(chat, "XHODD")
        await Client.send_message(chat, "TERII MAA")
        await Client.send_message(chat, "KA LUND")
        await Client.send_message(chat, "XHAKKE")
        await Client.send_message(chat, "TERIIIIII")
        await Client.send_message(chat, "MAA ")
        await Client.send_message(chat, "KA")
        await Client.send_message(chat, "BHOSDA")
        await Client.send_message(chat, "KI")
        await Client.send_message(chat, "MA")
        await Client.send_message(chat, "XHOD")
        await Client.send_message(chat, "DIYA")
        await Client.send_message(chat, "KI")
        await Client.send_message(chat, "MA")
        await Client.send_message(chat,  "RANDI")
        await Client.send_message(chat, "HIJDE")
        await Client.send_message(chat, "KA")
        await Client.send_message(chat, "BACCHA")
        await Client.send_message(chat, "TERI")
        await Client.send_message(chat, "MA")
        await Client.send_message(chat, "KI") 
        await Client.send_message(chat, "CHUDAI")
        await Client.send_message(chat, "KI") 
        await Client.send_message(chat, "STORY")
        await Client.send_message(chat, "PADEGA")
        await Client.send_message(chat, "BOL")
        await Client.send_message(chat, "RAMDI KE BACCHE")
        await Client.send_message(chat, "TRRI")
        await Client.send_message(chat,  "MA")
        await Client.send_message(chat, "KA")
        await Client.send_message(chat, "AASIQ")
        await Client.send_message(chat, "HOON")
        await Client.send_message(chat, "ME")
        await Client.send_message(chat, "TERI")
        await Client.send_message(chat,  "MA")                                                     
        await Client.send_message(chat,   "KA")
        await Client.send_message(chat, "GANG")
        await Client.send_message(chat, "BANG")
        await Client.send_message(chat, "KARDU")
        await Client.send_message(chat, "TERI")
        await Client.send_message(chat, "MA")
        await Client.send_message(chat, "KO")
        await Client.send_message(chat, "PREGNANT") 
        await Client.send_message(chat, "KARDU")
        await Client.send_message(chat, "TERI")
        await Client.send_message(chat, "BEHAN")
        await Client.send_message(chat, "KA")
        await Client.send_message(chat, "AASIQ") 
        await Client.send_message(chat, "HOON")   
        await Client.send_message(chat, "ME")
        await Client.send_message(chat, "TERI")
        await Client.send_message(chat, "MA")
        await Client.send_message(chat, "KI")
        await Client.send_message(chat, "PRICE")
        await Client.send_message(chat, "BOL")
        await Client.send_message(chat, "69$")
        await Client.send_message(chat, "DUNGA")
        await Client.send_message(chat, "ME")
        await Client.send_message(chat, "TU")
        await Client.send_message(chat, "BATA")
        await Client.send_message(chat, "KITNE")
        await Client.send_message(chat, "ME")
        await Client.send_message(chat, "DEGA")
        await Client.send_message(chat, "TERI")
        await Client.send_message(chat, " BEHAN KI")
        await Client.send_message(chat, "XHUT")
        await Client.send_message(chat, "TERI") 
        await Client.send_message(chat, "MA")
        await Client.send_message(chat, "KA")
        await Client.send_message(chat, "BHOSDA")
        await Client.send_message(chat, "FAT")
        await Client.send_message(chat, "GYA")
        await Client.send_message(chat, "JAAKE DEKH")
        await Client.send_message(chat,"TERI") 
        await Client.send_message(chat, "CHACHI")
        await Client.send_message(chat, "KO")
        await Client.send_message(chat,"BAGHA")
        await Client.send_message(chat, "LE")
        await Client.send_message(chat, "JAAU")
        await Client.send_message(chat, "BATA")
        await Client.send_message(chat, "LAWDE ")
        await Client.send_message(chat, "TERI")
        await Client.send_message(chat, "BEHAN")
        await Client.send_message(chat, "KO")
        await Client.send_message(chat, "OYO") 
        await Client.send_message(chat, "ME")
        await Client.send_message(chat, "CHODU")
        await Client.send_message(chat, "RANDI")
        await Client.send_message(chat, "KE")
        await Client.send_message(chat, "BACCHE")
        await Client.send_message(chat, "DEMON")
        await Client.send_message(chat, "OR")
        await Client.send_message(chat, "TERI")
        await Client.send_message(chat, "MA")
        await Client.send_message(chat, "KA")
        await Client.send_message(chat, "BHOSDA")
        await Client.send_message(chat, "CHODU")
        await Client.send_message(chat, "GAY")
        await Client.send_message(chat, "KA")
        await Client.send_message(chat, "BACCHA")
        await Client.send_message(chat, "TERI")
        await Client.send_message(chat, "maa")
        await Client.send_message(chat, "KI")
        await Client.send_message(chat, "XHUT")
        await Client.send_message(chat, "me")
        await Client.send_message(chat, "SAANP")
        await Client.send_message(chat, "GUSED")
        await Client.send_message(chat, "DU")
        await Client.send_message(chat, "TERI")
        await Client.send_message(chat, "MA")
        await Client.send_message(chat, "KI")
        await Client.send_message(chat, "GILI")
        await Client.send_message(chat, "CHUT")
        await Client.send_message(chat, "HAHAHAHAH")
        await Client.send_message(chat, "ABH")
        await Client.send_message(chat, "BOLDE")
        await Client.send_message(chat, "KI")
        await Client.send_message(chat, "TERII")
        await Client.send_message(chat, "MAA")
        await Client.send_message(chat, "RANDI")   
        await Client.send_message(chat, "H")
        await Client.send_message(chat, "KE")
        await Client.send_message(chat, "TATTE")
        await Client.send_message(chat, "TERI")
        await Client.send_message(chat, "MAA")
        await Client.send_message(chat, "KE")
        await Client.send_message(chat,  "SAATH")
        await Client.send_message(chat,  "SOJAAU")
        await Client.send_message(chat, "EK")
        await Client.send_message(chat, "NIGHT")
        await Client.send_message(chat, "BATA")
        await Client.send_message(chat, "BEHAN")
        await Client.send_message(chat, "KE")
        await Client.send_message(chat, "LODE")
        await Client.send_message(chat, "TERI")
        await Client.send_message(chat, "MA")
        await Client.send_message(chat, "KI")
        await Client.send_message(chat, "NANGI")
        await Client.send_message(chat, "XHUT")
        await Client.send_message(chat, "ME")
        await Client.send_message(chat, "AALU")
        await Client.send_message(chat, "BAMB")
        await Client.send_message(chat, "BAXXHA")
        await Client.send_message(chat, "H")
        await Client.send_message(chat, "TU")
        await Client.send_message(chat, " HAHAHAHAHA")
        await Client.send_message(chat, "BAAP")
        await Client.send_message(chat, "SE")
        await Client.send_message(chat, "LADEGA")
        await Client.send_message(chat, "ABH")
        await Client.send_message(chat, "TU")
        await Client.send_message(chat, "AUKAT")
        await Client.send_message(chat, "BANA")
        await Client.send_message(chat, "KIDXXX")
        await Client.send_message(chat, "TERI")
        await Client.send_message(chat, "MA")
        await Client.send_message(chat, "KA")
        await Client.send_message(chat, "RAPE")
        await Client.send_message(chat, "KARXUNGA")
        await Client.send_message(chat, "VERNA")
        await Client.send_message(chat, "HIHIHIHIHI")
        await Client.send_message(chat, "XHUD")
        await Client.send_message(chat, "GYI")
        await Client.send_message(chat, "TERI")
        await Client.send_message(chat, "MUMMY")
        await Client.send_message(chat, "ABH")
        await Client.send_message(chat, "AAA")
        await Client.send_message(chat, "TU")
        await Client.send_message(chat, "SPEED")
        await Client.send_message(chat, "COVER")
        await Client.send_message(chat, "KAR")
        await Client.send_message(chat, "BAS")
        await Client.send_message(chat, "TERI")
        await Client.send_message(chat, "MUMMY")
        await Client.send_message(chat, "XHOD")
        await Client.send_message(chat, "DUNGA")
        await Client.send_message(chat, "TERI")
        await Client.send_message(chat, " AMMA")
        await Client.send_message(chat, "KA")
        await Client.send_message(chat, "AASIQ")
        await Client.send_message(chat, "BOL")
        await Client.send_message(chat, "MEKO")
        await Client.send_message(chat, "HAHAHAH")
        await Client.send_message(chat, "XHUD GYA")
        await Client.send_message(chat, "TU")
        await Client.send_message(chat, "TERA")
        await Client.send_message(chat, "KHANDAAN")
        await Client.send_message(chat, "XHOD")
        await Client.send_message(chat, "DAALA")
        await Client.send_message(chat, "TERI")
        await Client.send_message(chat, "BIWI")
        await Client.send_message(chat, "KI")
        await Client.send_message(chat, "XHUT")
        await Client.send_message(chat, "SE")
        await Client.send_message(chat, "BACCHA")
        await Client.send_message(chat, "NIKAL") 
        await Client.send_message(chat, "JAYEGAA")
        await Client.send_message(chat, "KALAP MAT")
        await Client.send_message(chat, "TERI")
        await Client.send_message(chat, "MAA")
        await Client.send_message(chat, "SE")
        await Client.send_message(chat, "POOXH")
        await Client.send_message(chat, "KI")
        await Client.send_message(chat, "TERA")
        await Client.send_message(chat, "ASLI")
        await Client.send_message(chat, "BAAP")
        await Client.send_message(chat, "KON")
        await Client.send_message(chat, "H")
        await Client.send_message(chat, "TERII")
        await Client.send_message(chat, "MUMMY")
        await Client.send_message(chat, "KI") 
        await Client.send_message(chat, "XHUT")
        await Client.send_message(chat, "ME")
        await Client.send_message(chat, "SODA")
        await Client.send_message(chat, "GUSED")
        await Client.send_message(chat, "DU")
        await Client.send_message(chat, "TERI")
        await Client.send_message(chat, "BEHAN")
        await Client.send_message(chat, "KI")
        await Client.send_message(chat, "XHUT")
        await Client.send_message(chat, "me")
        await Client.send_message(chat, "LIGHT")
        await Client.send_message(chat, "BULB")
        await Client.send_message(chat, "DAAL")
        await Client.send_message(chat, "KE")
        await Client.send_message(chat, "SWITCH")
        await Client.send_message(chat, "ON") 
        await Client.send_message(chat, "KARDU")
        await Client.send_message(chat, "TERE")
        await Client.send_message(chat, "BAAP")
        await Client.send_message(chat, "KI")
        await Client.send_message(chat, "MUMMY")
        await Client.send_message(chat,  "KE")
        await Client.send_message(chat, "BETE")
        await Client.send_message(chat, "KI")
        await Client.send_message(chat, "BETI")
        await Client.send_message(chat, "XHOD")
        await Client.send_message(chat, "du")
        await Client.send_message(chat, "TERI")
        await Client.send_message(chat, "MA")
        await Client.send_message(chat, "KI")
        await Client.send_message(chat, "CHUT")
        await Client.send_message(chat, "ME")
        await Client.send_message(chat, "LODA")
        await Client.send_message(chat, "DAAL")
        await Client.send_message(chat, "KE")
        await Client.send_message(chat, "MUTH")
        await Client.send_message(chat, "MAARDU")
        await Client.send_message(chat, "TERI")
        await Client.send_message(chat, "MAAAA")
        await Client.send_message(chat, "BEHAN")
        await Client.send_message(chat, "RANDI")
        await Client.send_message(chat, "TERA")
        await Client.send_message(chat, "PURA")
        await Client.send_message(chat, "KHANDAAN")
        await Client.send_message(chat, "XHOD")
        await Client.send_message(chat, "DAALA")
        await Client.send_message(chat, "HAHAHAHAH")

