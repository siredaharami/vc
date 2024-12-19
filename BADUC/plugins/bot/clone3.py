import logging
import os
import asyncio
from pyrogram.enums import ParseMode
from pyrogram import Client, filters
from pyrogram.errors.exceptions.bad_request_400 import AccessTokenExpired, AccessTokenInvalid
from pyrogram.types import BotCommand
from BADUC.core.config import API_HASH, API_ID, OWNER_ID
from BADUC import CLONE_OWNERS
from BADUC.core.clients import bot
from BADUC import mongodb

CLONES = set()
cloneownerdb = mongodb.cloneownerdb
clonebotdb = mongodb.clonebotdb

async def save_clonebot_owner(bot_id, user_id):
    await cloneownerdb.insert_one({"bot_id": bot_id, "user_id": user_id})

@bot.on_message(filters.command(["clone", "host", "deploy"]))
async def clone_txt(client, message):
    if len(message.command) > 1:
        bot_token = message.text.split("/clone", 1)[1].strip()
        mi = await message.reply_text("ᴘʟᴇᴀꜱᴇ ᴡᴀɪᴛ ᴡʜɪʟᴇ ɪ ᴄʜᴇᴄᴋ ᴛʜᴇ ʙᴏᴛ ᴛᴏᴋᴇɴ.")
        try:
            ai = Client(bot_token, API_ID, API_HASH, bot_token=bot_token, plugins=dict(root="shizuchat/plugin"))
            await ai.start()
            bot = await ai.get_me()
            bot_id = bot.id
            user_id = message.from_user.id
            CLONE_OWNERS[bot_id] = user_id
            await ai.set_bot_commands([
                BotCommand("start", "✧ sᴛᴀʀᴛ ᴛʜᴇ ʙᴏᴛ ✧"),
                BotCommand("help", "✧ ɢᴇᴛ ᴛʜᴇ ʜᴇʟᴘ ᴍᴇɴᴜ ✧"),
                BotCommand("ping", "✧ ᴄʜᴇᴄᴋ ɪғ ᴛʜᴇ ʙᴏᴛ ɪs ᴀʟɪᴠᴇ ᴏʀ ᴅᴇsᴅ ✧"),
                BotCommand("shipping", "✧ ᴄᴏᴜᴘʟᴇs ᴏғ ᴅᴀʏ ✧"),
                BotCommand("rankings", "✧ ᴜsᴇʀ ᴍsɢ ʟᴇᴀᴅᴇʀʙᴏᴀʀᴅ ✧"),
            ])
        except (AccessTokenExpired, AccessTokenInvalid):
            await mi.edit_text("ɪɴᴠᴀʟɪᴅ ʙᴏᴛ ᴛᴏᴋᴇɴ. ᴘʟᴇᴀꜱᴇ ᴘʀᴏᴠɪᴅᴇ ᴀ ᴠᴀʟɪᴅ ᴏɴᴇ.")
            return
        except Exception as e:
            cloned_bot = await clonebotdb.find_one({"token": bot_token})
            if cloned_bot:
                await mi.edit_text(" ʏᴏᴜʀ ʙᴏᴛ ɪꜱ ᴀʟʀᴇᴀᴅʏ ᴄʟᴏɴᴇᴅ ❤️")
                return

        await mi.edit_text("ᴄʟᴏɴɪɴɢ ᴘʀᴏᴄᴇꜱꜱ ꜱᴛᴀʀᴛᴇᴅ. ᴘʟᴇᴀꜱᴇ ᴡᴀɪᴛ ꜰᴏʀ ᴛʜᴇ ʙᴏᴛ ᴛᴏ ꜱᴛᴀʀᴛ.")
        try:
            details = {
                "bot_id": bot.id,
                "is_bot": True,
                "user_id": user_id,
                "name": bot.first_name,
                "token": bot_token,
                "username": bot.username,
            }
            cloned_bots = clonebotdb.find()
            cloned_bots_list = await cloned_bots.to_list(length=None)
            total_clones = len(cloned_bots_list)
            
            await bot.send_message(
                int(OWNER_ID), f"ɴᴇᴡ~ᴄʟᴏɴᴇ\n\nʙᴏᴛ:- @{bot.username}**\n\nᴅᴇᴛᴀɪʟs:-**\n{details}"
            )

            await clonebotdb.insert_one(details)
            
            CLONES.add(bot.id)

            await mi.edit_text(
                f"ʙᴏᴛ @{bot.username} ʜᴀꜱ ʙᴇᴇɴ ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ ᴄʟᴏɴᴇᴅ ᴀɴᴅ ꜱᴛᴀʀᴛᴇᴅ ✅.\nʀᴇᴍᴏᴠᴇ ᴄʟᴏɴᴇ ʙʏ :- /delclone\nᴄʜᴇᴄᴋ ᴀʟʟ ᴄʟᴏɴᴇᴅ ʙᴏᴛ ʟɪꜱᴛ ʙʏ:- /cloned"
            )
        except BaseException as e:
            logging.exception("ᴇʀʀᴏʀ ᴡʜɪʟᴇ ᴄʟᴏɴɪɴɢ ʙᴏᴛ.")
            await mi.edit_text(
                f"⚠️ <b>Error:</b>\n\n<code>{e}</code>\n\nꜰᴏʀᴡᴀʀᴅ ᴛʜɪꜱ ᴍᴇꜱꜱᴀɢᴇ ᴛᴏ @PBX_CHAT ꜰᴏʀ ᴀꜱꜱɪꜱᴛᴀɴᴄᴇ"
            )
    else:
        await message.reply_text("ᴘʀᴏᴠɪᴅᴇ ʙᴏᴛ ᴛᴏᴋᴇɴ ᴀꜰᴛᴇʀ /clone ᴄᴏᴍᴍᴀɴᴅ ꜰʀᴏᴍ @Botfather.")

@bot.on_message(filters.command("cloned"))
async def list_cloned_bots(client, message):
    try:
        cloned_bots = clonebotdb.find()
        cloned_bots_list = await cloned_bots.to_list(length=None)
        if not cloned_bots_list:
            await message.reply_text("ɴᴏ ʙᴏᴛꜱ ʜᴀᴠᴇ ʙᴇᴇɴ ᴄʟᴏɴᴇᴅ ʏᴇᴛ.")
            return
        total_clones = len(cloned_bots_list)
        text = f"**Total Cloned Bots:** {total_clones}\n\n"
        for bot in cloned_bots_list:
            text += f"**Bot ID:** `{bot['bot_id']}`\n"
            text += f"**Bot Name:** {bot['name']}\n"
            text += f"**Bot Username:** @{bot['username']}\n\n"
        await message.reply_text(text)
    except Exception as e:
        logging.exception(e)
        await message.reply_text("ᴀɴ ᴇʀʀᴏʀ ᴏᴄᴄᴜʀʀᴇᴅ ᴡʜɪʟᴇ ʟɪꜱᴛɪɴɢ ᴄʟᴏɴᴇᴅ ʙᴏᴛꜱ.")

@bot.on_message(
    filters.command(["deletecloned", "delcloned", "delclone", "deleteclone", "removeclone", "cancelclone"])
)
async def delete_cloned_bot(client, message):
    try:
        if len(message.command) < 2:
            await message.reply_text("⚠️ ᴘʟᴇᴀꜱᴇ ᴘʀᴏᴠɪᴅᴇ ᴛʜᴇ ʙᴏᴛ ᴛᴏᴋᴇɴ ᴀꜰᴛᴇʀ ᴛʜᴇ ᴄᴏᴍᴍᴀɴᴅ.")
            return

        bot_token = " ".join(message.command[1:])
        ok = await message.reply_text("ᴄʜᴇᴄᴋɪɴɢ ᴛʜᴇ ʙᴏᴛ ᴛᴏᴋᴇɴ...")

        cloned_bot = await clonebotdb.find_one({"token": bot_token})
        if cloned_bot:
            await clonebotdb.delete_one({"token": bot_token})
            CLONES.remove(cloned_bot["bot_id"])
            await ok.edit_text(
                "🤖 ʏᴏᴜʀ ᴄʟᴏɴᴇᴅ ʙᴏᴛ ʜᴀꜱ ʙᴇᴇɴ ʀᴇᴍᴏᴠᴇᴅ ꜰʀᴏᴍ ᴍʏ ᴅᴀᴛᴀʙᴀꜱᴇ ✅\n🔄 ᴋɪɴᴅʟʏ ʀᴇᴠᴏᴋᴇ ʏᴏᴜʀ ʙᴏᴛ ᴛᴏᴋᴇɴ ꜰʀᴏᴍ @botfather ᴏᴛʜᴇʀᴡɪꜱᴇ ʏᴏᴜʀ ʙᴏᴛ ᴡɪʟʟ ꜱᴛᴏᴘ ᴡʜᴇɴ @{bot.username} ᴡɪʟʟ ʀᴇꜱᴛᴀʀᴛ ☠️"
            )
            os.system(f"kill -9 {os.getpid()} && bash start")
        else:
            await message.reply_text("⚠️ ᴛʜᴇ ᴘʀᴏᴠɪᴅᴇᴅ ʙᴏᴛ ᴛᴏᴋᴇɴ ɪꜱ ɴᴏᴛ ɪɴ ᴛʜᴇ ᴄʟᴏɴᴇᴅ ʟɪꜱᴛ.")
    except Exception as e:
        await message.reply_text(f"ᴀɴ ᴇʀʀᴏʀ ᴏᴄᴄᴜʀʀᴇᴅ ᴡʜɪʟᴇ ᴅᴇʟᴇᴛɪɴɢ ᴛʜᴇ ᴄʟᴏɴᴇᴅ ʙᴏᴛ: {e}")
        logging.exception(e)


async def restart_bots():
    global CLONES
    try:
        logging.info("ʀᴇꜱᴛᴀʀᴛɪɴɢ ᴀʟʟ ᴄʟᴏɴᴇᴅ ʙᴏᴛꜱ...")
        bots = [bot async for bot in clonebotdb.find()]
        
        async def restart_bot(bot):
            bot_token = bot["token"]
            ai = Client(bot_token, API_ID, API_HASH, bot_token=bot_token, plugins=dict(root="shizuchat/plugin"))
            try:
                await ai.start()
                bot_info = await ai.get_me()
                await ai.set_bot_commands([
                    BotCommand("start", "✧ sᴛᴀʀᴛ ᴛʜᴇ ʙᴏᴛ ✧"),
                BotCommand("help", "✧ ɢᴇᴛ ᴛʜᴇ ʜᴇʟᴘ ᴍᴇɴᴜ ✧"),
                BotCommand("ping", "✧ ᴄʜᴇᴄᴋ ɪғ ᴛʜᴇ ʙᴏᴛ ɪs ᴀʟɪᴠᴇ ᴏʀ ᴅᴇsᴅ ✧"),
                BotCommand("shipping", "✧ ᴄᴏᴜᴘʟᴇs ᴏғ ᴅᴀʏ ✧"),
                BotCommand("rankings", "✧ ᴜsᴇʀ ᴍsɢ ʟᴇᴀᴅᴇʀʙᴏᴀʀᴅ ✧"),
            ])

                if bot_info.id not in CLONES:
                    CLONES.add(bot_info.id)
                    
            except (AccessTokenExpired, AccessTokenInvalid):
                await clonebotdb.delete_one({"token": bot_token})
                logging.info(f"ʀᴇᴍᴏᴠᴇᴅ ᴇxᴘɪʀᴇᴅ ᴏʀ ɪɴᴠᴀʟɪᴅ ᴛᴏᴋᴇɴ ꜰᴏʀ ʙᴏᴛ ɪᴅ: {bot['bot_id']}")
            except Exception as e:
                logging.exception(f"ᴇʀʀᴏʀ ᴡʜɪʟᴇ ʀᴇꜱᴛᴀʀᴛɪɴɢ ʙᴏᴛ ᴡɪᴛʜ ᴛᴏᴋᴇɴ {bot_token}: {e}")
            
        await asyncio.gather(*(restart_bot(bot) for bot in bots))
        
    except Exception as e:
        logging.exception("ᴇʀʀᴏʀ ᴡʜɪʟᴇ ʀᴇꜱᴛᴀʀᴛɪɴɢ ʙᴏᴛꜱ.")


@bot.on_message(filters.command("delallclone") & filters.user(int(OWNER_ID)))
async def delete_all_cloned_bots(client, message):
    try:
        a = await message.reply_text("ᴅᴇʟᴇᴛɪɴɢ ᴀʟʟ ᴄʟᴏɴᴇᴅ ʙᴏᴛꜱ...")
        await clonebotdb.delete_many({})
        CLONES.clear()
        await a.edit_text("ᴀʟʟ ᴄʟᴏɴᴇᴅ ʙᴏᴛꜱ ʜᴀᴠᴇ ʙᴇᴇɴ ᴅᴇʟᴇᴛᴇᴅ ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ ✅")
        os.system(f"kill -9 {os.getpid()} && bash start")
    except Exception as e:
        await a.edit_text(f"ᴀɴ ᴇʀʀᴏʀ ᴏᴄᴄᴜʀʀᴇᴅ ᴡʜɪʟᴇ ᴅᴇʟᴇᴛɪɴɢ ᴀʟʟ ᴄʟᴏɴᴇᴅ ʙᴏᴛꜱ. {e}")
        logging.exception(e)

  
