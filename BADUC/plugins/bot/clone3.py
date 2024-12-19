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

# Global Variables
CLONES = set()
cloneownerdb = mongodb.cloneownerdb
clonebotdb = mongodb.clonebotdb

# Initialize Logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

async def initialize_clones():
    """
    Initialize the list of cloned bots at startup.
    """
    global CLONES
    cloned_bots = [bot async for bot in clonebotdb.find()]
    CLONES = {bot["bot_id"] for bot in cloned_bots}
    logging.info(f"Initialized {len(CLONES)} cloned bots.")

async def save_clonebot_owner(bot_id, user_id):
    """
    Save the bot owner details to the database.
    """
    await cloneownerdb.insert_one({"bot_id": bot_id, "user_id": user_id})

@bot.on_message(filters.command(["clone", "host", "deploy"]))
async def clone_txt(client, message):
    if len(message.command) > 1:
        bot_token = message.text.split("/clone", 1)[1].strip()
        mi = await message.reply_text("ᴘʟᴇᴀꜱᴇ ᴡᴀɪᴛ ᴡʜɪʟᴇ ɪ ᴄʜᴇᴄᴋ ᴛʜᴇ ʙᴏᴛ ᴛᴏᴋᴇɴ.")
        try:
            ai = Client(bot_token, API_ID, API_HASH, bot_token=bot_token, plugins=dict(root="BADUC/plugins/clone2"))
            await ai.start()
            bot = await ai.get_me()
            bot_id = bot.id
            user_id = message.from_user.id

            # Save the bot owner details
            CLONE_OWNERS[bot_id] = user_id
            await save_clonebot_owner(bot_id, user_id)

            # Set bot commands
            await ai.set_bot_commands([
                BotCommand("start", "✧ sᴛᴀʀᴛ ᴛʜᴇ ʙᴏᴛ ✧"),
                BotCommand("help", "✧ ɢᴇᴛ ᴛʜᴇ ʜᴇʟᴘ ᴍᴇɴᴜ ✧"),
                BotCommand("ping", "✧ ᴄʜᴇᴄᴋ ɪғ ᴛʜᴇ ʙᴏᴛ ɪꜱ ᴀʟɪᴠᴇ ✧"),
                BotCommand("shipping", "✧ ᴄᴏᴜᴘʟᴇꜱ ᴏғ ᴅᴀʏ ✧"),
                BotCommand("rankings", "✧ ᴜꜱᴇʀ ᴍꜱɢ ʟᴇᴀᴅᴇʀʙᴏᴀʀᴅ ✧"),
            ])

            # Save cloned bot details
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

            await bot.send_message(
                int(OWNER_ID), f"ɴᴇᴡ~ᴄʟᴏɴᴇ\n\nʙᴏᴛ:- @{bot.username}\n\nᴅᴇᴛᴀɪʟꜱ:-\n{details}"
            )
            await clonebotdb.insert_one(details)
            CLONES.add(bot.id)

            await mi.edit_text(
                f"ʙᴏᴛ @{bot.username} ʜᴀꜱ ʙᴇᴇɴ ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ ᴄʟᴏɴᴇᴅ ✅."
            )
        except (AccessTokenExpired, AccessTokenInvalid):
            await mi.edit_text("ɪɴᴠᴀʟɪᴅ ʙᴏᴛ ᴛᴏᴋᴇɴ. ᴘʟᴇᴀꜱᴇ ᴘʀᴏᴠɪᴅᴇ ᴀ ᴠᴀʟɪᴅ ᴏɴᴇ.")
        except Exception as e:
            logging.exception("Error while cloning bot.")
            await mi.edit_text(f"⚠️ <b>Error:</b>\n\n<code>{e}</code>")
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

@bot.on_message(filters.command(["delclone", "deleteclone"]))
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
            await ok.edit_text("🤖 ʏᴏᴜʀ ᴄʟᴏɴᴇᴅ ʙᴏᴛ ʜᴀꜱ ʙᴇᴇɴ ʀᴇᴍᴏᴠᴇᴅ ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ ✅.")
        else:
            await message.reply_text("⚠️ ᴛʜᴇ ᴘʀᴏᴠɪᴅᴇᴅ ʙᴏᴛ ᴛᴏᴋᴇɴ ɪꜱ ɴᴏᴛ ɪɴ ᴛʜᴇ ᴄʟᴏɴᴇᴅ ʟɪꜱᴛ.")
    except Exception as e:
        await message.reply_text(f"ᴀɴ ᴇʀʀᴏʀ ᴏᴄᴄᴜʀʀᴇᴅ ᴡʜɪʟᴇ ᴅᴇʟᴇᴛɪɴɢ ᴛʜᴇ ᴄʟᴏɴᴇᴅ ʙᴏᴛ: {e}")
        logging.exception(e)

if __name__ == "__main__":
    asyncio.run(initialize_clones())
    try:
        logging.info("Starting the bot...")
        bot.run()
    except KeyboardInterrupt:
        logging.info("Bot stopped manually.")
    except Exception as e:
        logging.exception("Unexpected error occurred.")
