from BADUC import SUDOERS
from BADUC.core.clients import app
from BADUC.core.command import *

from pyrogram import Client
from pyrogram.types import Message
from pyrogram.enums import ChatAction
from pyrogram import Client, filters

from asyncio import sleep

x = True

@app.on_message(bad(["stopbigspam"]) & (filters.me | filters.user(SUDOERS)))
async def stopbigspam(c: Client, m: Message):
    await c.send_chat_action(m.chat.id, ChatAction.CANCEL)
    await m.reply_text("Stopped big spam")
    global x
    x = False



@app.on_message(bad(["bigspam"]) & (filters.me | filters.user(SUDOERS)))
async def start_big_spam(c: Client, m: Message):
    xn = await m.reply_text("Startting galispam")
    await sleep(0.4)
    await xn.delete()
    await c.send_chat_action(m.chat.id,ChatAction.TYPING)
    while x == True:
        await m.delete()
        chat = m.chat.id
        await app.send_message(chat, "SHURU")
        await app.send_message(chat, "KARU")
        await app.send_message(chat, "TERI XHUDAI")
        await app.send_message(chat, "TERIII")
        await app.send_message(chat, "MA")
        await app.send_message(chat, "KI")
        await app.send_message(chat, "XHUT")
        await app.send_message(chat, "XHODD")
        await app.send_message(chat, "TERII MAA")
        await app.send_message(chat, "KA LUND")
        await app.send_message(chat, "XHAKKE")
        await app.send_message(chat, "TERIIIIII")
        await app.send_message(chat, "MAA ")
        await app.send_message(chat, "KA")
        await app.send_message(chat, "BHOSDA")
        await app.send_message(chat, "KI")
        await app.send_message(chat, "MA")
        await app.send_message(chat, "XHOD")
        await app.send_message(chat, "DIYA")
        await app.send_message(chat, "KI")
        await app.send_message(chat, "MA")
        await app.send_message(chat,  "RANDI")
        await app.send_message(chat, "HIJDE")
        await app.send_message(chat, "KA")
        await app.send_message(chat, "BACCHA")
        await app.send_message(chat, "TERI")
        await app.send_message(chat, "MA")
        await app.send_message(chat, "KI") 
        await app.send_message(chat, "CHUDAI")
        await app.send_message(chat, "KI") 
        await app.send_message(chat, "STORY")
        await app.send_message(chat, "PADEGA")
        await app.send_message(chat, "BOL")
        await app.send_message(chat, "RAMDI KE BACCHE")
        await app.send_message(chat, "TRRI")
        await app.send_message(chat,  "MA")
        await app.send_message(chat, "KA")
        await app.send_message(chat, "AASIQ")
        await app.send_message(chat, "HOON")
        await app.send_message(chat, "ME")
        await app.send_message(chat, "TERI")
        await app.send_message(chat,  "MA")                                                     
        await app.send_message(chat,   "KA")
        await app.send_message(chat, "GANG")
        await app.send_message(chat, "BANG")
        await app.send_message(chat, "KARDU")
        await app.send_message(chat, "TERI")
        await app.send_message(chat, "MA")
        await app.send_message(chat, "KO")
        await app.send_message(chat, "PREGNANT") 
        await app.send_message(chat, "KARDU")
        await app.send_message(chat, "TERI")
        await app.send_message(chat, "BEHAN")
        await app.send_message(chat, "KA")
        await app.send_message(chat, "AASIQ") 
        await app.send_message(chat, "HOON")   
        await app.send_message(chat, "ME")
        await app.send_message(chat, "TERI")
        await app.send_message(chat, "MA")
        await app.send_message(chat, "KI")
        await app.send_message(chat, "PRICE")
        await app.send_message(chat, "BOL")
        await app.send_message(chat, "69$")
        await app.send_message(chat, "DUNGA")
        await app.send_message(chat, "ME")
        await app.send_message(chat, "TU")
        await app.send_message(chat, "BATA")
        await app.send_message(chat, "KITNE")
        await app.send_message(chat, "ME")
        await app.send_message(chat, "DEGA")
        await app.send_message(chat, "TERI")
        await app.send_message(chat, " BEHAN KI")
        await app.send_message(chat, "XHUT")
        await app.send_message(chat, "TERI") 
        await app.send_message(chat, "MA")
        await app.send_message(chat, "KA")
        await app.send_message(chat, "BHOSDA")
        await app.send_message(chat, "FAT")
        await app.send_message(chat, "GYA")
        await app.send_message(chat, "JAAKE DEKH")
        await app.send_message(chat,"TERI") 
        await app.send_message(chat, "CHACHI")
        await app.send_message(chat, "KO")
        await app.send_message(chat,"BAGHA")
        await app.send_message(chat, "LE")
        await app.send_message(chat, "JAAU")
        await app.send_message(chat, "BATA")
        await app.send_message(chat, "LAWDE ")
        await app.send_message(chat, "TERI")
        await app.send_message(chat, "BEHAN")
        await app.send_message(chat, "KO")
        await app.send_message(chat, "OYO") 
        await app.send_message(chat, "ME")
        await app.send_message(chat, "CHODU")
        await app.send_message(chat, "RANDI")
        await app.send_message(chat, "KE")
        await app.send_message(chat, "BACCHE")
        await app.send_message(chat, "DEMON")
        await app.send_message(chat, "OR")
        await app.send_message(chat, "TERI")
        await app.send_message(chat, "MA")
        await app.send_message(chat, "KA")
        await app.send_message(chat, "BHOSDA")
        await app.send_message(chat, "CHODU")
        await app.send_message(chat, "GAY")
        await app.send_message(chat, "KA")
        await app.send_message(chat, "BACCHA")
        await app.send_message(chat, "TERI")
        await app.send_message(chat, "maa")
        await app.send_message(chat, "KI")
        await app.send_message(chat, "XHUT")
        await app.send_message(chat, "me")
        await app.send_message(chat, "SAANP")
        await app.send_message(chat, "GUSED")
        await app.send_message(chat, "DU")
        await app.send_message(chat, "TERI")
        await app.send_message(chat, "MA")
        await app.send_message(chat, "KI")
        await app.send_message(chat, "GILI")
        await app.send_message(chat, "CHUT")
        await app.send_message(chat, "HAHAHAHAH")
        await app.send_message(chat, "ABH")
        await app.send_message(chat, "BOLDE")
        await app.send_message(chat, "KI")
        await app.send_message(chat, "TERII")
        await app.send_message(chat, "MAA")
        await app.send_message(chat, "RANDI")   
        await app.send_message(chat, "H")
        await app.send_message(chat, "KE")
        await app.send_message(chat, "TATTE")
        await app.send_message(chat, "TERI")
        await app.send_message(chat, "MAA")
        await app.send_message(chat, "KE")
        await app.send_message(chat,  "SAATH")
        await app.send_message(chat,  "SOJAAU")
        await app.send_message(chat, "EK")
        await app.send_message(chat, "NIGHT")
        await app.send_message(chat, "BATA")
        await app.send_message(chat, "BEHAN")
        await app.send_message(chat, "KE")
        await app.send_message(chat, "LODE")
        await app.send_message(chat, "TERI")
        await app.send_message(chat, "MA")
        await app.send_message(chat, "KI")
        await app.send_message(chat, "NANGI")
        await app.send_message(chat, "XHUT")
        await app.send_message(chat, "ME")
        await app.send_message(chat, "AALU")
        await app.send_message(chat, "BAMB")
        await app.send_message(chat, "BAXXHA")
        await app.send_message(chat, "H")
        await app.send_message(chat, "TU")
        await app.send_message(chat, " HAHAHAHAHA")
        await app.send_message(chat, "BAAP")
        await app.send_message(chat, "SE")
        await app.send_message(chat, "LADEGA")
        await app.send_message(chat, "ABH")
        await app.send_message(chat, "TU")
        await app.send_message(chat, "AUKAT")
        await app.send_message(chat, "BANA")
        await app.send_message(chat, "KIDXXX")
        await app.send_message(chat, "TERI")
        await app.send_message(chat, "MA")
        await app.send_message(chat, "KA")
        await app.send_message(chat, "RAPE")
        await app.send_message(chat, "KARXUNGA")
        await app.send_message(chat, "VERNA")
        await app.send_message(chat, "HIHIHIHIHI")
        await app.send_message(chat, "XHUD")
        await app.send_message(chat, "GYI")
        await app.send_message(chat, "TERI")
        await app.send_message(chat, "MUMMY")
        await app.send_message(chat, "ABH")
        await app.send_message(chat, "AAA")
        await app.send_message(chat, "TU")
        await app.send_message(chat, "SPEED")
        await app.send_message(chat, "COVER")
        await app.send_message(chat, "KAR")
        await app.send_message(chat, "BAS")
        await app.send_message(chat, "TERI")
        await app.send_message(chat, "MUMMY")
        await app.send_message(chat, "XHOD")
        await app.send_message(chat, "DUNGA")
        await app.send_message(chat, "TERI")
        await app.send_message(chat, " AMMA")
        await app.send_message(chat, "KA")
        await app.send_message(chat, "AASIQ")
        await app.send_message(chat, "BOL")
        await app.send_message(chat, "MEKO")
        await app.send_message(chat, "HAHAHAH")
        await app.send_message(chat, "XHUD GYA")
        await app.send_message(chat, "TU")
        await app.send_message(chat, "TERA")
        await app.send_message(chat, "KHANDAAN")
        await app.send_message(chat, "XHOD")
        await app.send_message(chat, "DAALA")
        await app.send_message(chat, "TERI")
        await app.send_message(chat, "BIWI")
        await app.send_message(chat, "KI")
        await app.send_message(chat, "XHUT")
        await app.send_message(chat, "SE")
        await app.send_message(chat, "BACCHA")
        await app.send_message(chat, "NIKAL") 
        await app.send_message(chat, "JAYEGAA")
        await app.send_message(chat, "KALAP MAT")
        await app.send_message(chat, "TERI")
        await app.send_message(chat, "MAA")
        await app.send_message(chat, "SE")
        await app.send_message(chat, "POOXH")
        await app.send_message(chat, "KI")
        await app.send_message(chat, "TERA")
        await app.send_message(chat, "ASLI")
        await app.send_message(chat, "BAAP")
        await app.send_message(chat, "KON")
        await app.send_message(chat, "H")
        await app.send_message(chat, "TERII")
        await app.send_message(chat, "MUMMY")
        await app.send_message(chat, "KI") 
        await app.send_message(chat, "XHUT")
        await app.send_message(chat, "ME")
        await app.send_message(chat, "SODA")
        await app.send_message(chat, "GUSED")
        await app.send_message(chat, "DU")
        await app.send_message(chat, "TERI")
        await app.send_message(chat, "BEHAN")
        await app.send_message(chat, "KI")
        await app.send_message(chat, "XHUT")
        await app.send_message(chat, "me")
        await app.send_message(chat, "LIGHT")
        await app.send_message(chat, "BULB")
        await app.send_message(chat, "DAAL")
        await app.send_message(chat, "KE")
        await app.send_message(chat, "SWITCH")
        await app.send_message(chat, "ON") 
        await app.send_message(chat, "KARDU")
        await app.send_message(chat, "TERE")
        await app.send_message(chat, "BAAP")
        await app.send_message(chat, "KI")
        await app.send_message(chat, "MUMMY")
        await app.send_message(chat,  "KE")
        await app.send_message(chat, "BETE")
        await app.send_message(chat, "KI")
        await app.send_message(chat, "BETI")
        await app.send_message(chat, "XHOD")
        await app.send_message(chat, "du")
        await app.send_message(chat, "TERI")
        await app.send_message(chat, "MA")
        await app.send_message(chat, "KI")
        await app.send_message(chat, "CHUT")
        await app.send_message(chat, "ME")
        await app.send_message(chat, "LODA")
        await app.send_message(chat, "DAAL")
        await app.send_message(chat, "KE")
        await app.send_message(chat, "MUTH")
        await app.send_message(chat, "MAARDU")
        await app.send_message(chat, "TERI")
        await app.send_message(chat, "MAAAA")
        await app.send_message(chat, "BEHAN")
        await app.send_message(chat, "RANDI")
        await app.send_message(chat, "TERA")
        await app.send_message(chat, "PURA")
        await app.send_message(chat, "KHANDAAN")
        await app.send_message(chat, "XHOD")
        await app.send_message(chat, "DAALA")
        await app.send_message(chat, "HAHAHAHAH")

