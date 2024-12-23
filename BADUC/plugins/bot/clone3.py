import logging
import asyncio
import os
import subprocess
from pyrogram.enums import ParseMode
from pyrogram import Client, filters
from pyrogram.errors import PeerIdInvalid
from pyrogram.errors.exceptions.bad_request_400 import AccessTokenExpired, AccessTokenInvalid
from pyrogram.types import BotCommand
from BADUC.core.config import API_HASH, API_ID, OWNER_ID
from BADUC import CLONE_OWNERS
from BADUC.core.clients import bot
from BADUC import mongodb
from BADUC.core.command import *
from BADUC import SUDOERS

# Global Variables
CLONES = set()
cloneownerdb = mongodb.cloneownerdb
clonebotdb = mongodb.clonebotdb

# Initialize Logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

async def initialize_clones():
    global CLONES
    cloned_bots = [bot async for bot in clonebotdb.find()]
    CLONES = {bot["bot_id"] for bot in cloned_bots}
    logging.info(f"Initialized {len(CLONES)} cloned bots.")

async def save_clonebot_owner(bot_id, user_id):
    await cloneownerdb.insert_one({"bot_id": bot_id, "user_id": user_id})

async def get_bot_owner(bot_id):
    owner = await cloneownerdb.find_one({"bot_id": bot_id})
    return owner["user_id"] if owner else None

def is_authorized(bot_id, user_id):
    return CLONE_OWNERS.get(bot_id) == user_id

@bot.on_message(filters.command(["botclone"]))
async def clone_txt(client, message):
    if len(message.command) > 1:
        bot_token = message.text.split("/botclone", 1)[1].strip()
        mi = await message.reply_text("ᴘʟᴇᴀꜱᴇ ᴡᴀɪᴛ ᴡʜɪʟᴇ ɪ ᴄʜᴇᴄᴋ ᴛʜᴇ ʙᴏᴛ ᴛᴏᴋᴇɴ.")
        try:
            ai = Client(bot_token, API_ID, API_HASH, bot_token=bot_token, plugins=dict(root="BADUC/plugins/clone2"))
            await ai.start()
            bot = await ai.get_me()

            if not bot.is_bot:
                await mi.edit_text("⚠️ The provided token does not belong to a bot.")
                await ai.stop()
                return

            bot_id = bot.id
            user_id = message.from_user.id
            CLONE_OWNERS[bot_id] = user_id
            await save_clonebot_owner(bot_id, user_id)

            await ai.set_bot_commands([
                BotCommand("start", "✧ sᴛᴀʀᴛ ᴛʜᴇ ʙᴏᴛ ✧"),
                BotCommand("help", "✧ ɢᴇᴛ ᴛʜᴇ ʜᴇʟᴘ ᴍᴇɴᴜ ✧"),
                BotCommand("ping", "✧ ᴄʜᴇᴄᴋ ʙᴏᴛ ʀᴇꜱᴘᴏɴꜱᴇ ✧")
            ])

            details = {
                "bot_id": bot.id,
                "is_bot": True,
                "user_id": user_id,
                "name": bot.first_name,
                "token": bot_token,
                "username": bot.username,
            }

            await clonebotdb.insert_one(details)
            CLONES.add(bot.id)

            await mi.edit_text(
                f"ʙᴏᴛ @{bot.username} ʜᴀꜱ ʙᴇᴇɴ ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ ᴄʟᴏɴᴇᴅ."
            )
        except Exception as e:
            await mi.edit_text(f"[ʀᴏᴏᴛ]:: Error while cloning bot.\n\n**Error**: {e}")

@bot.on_message(filters.command("botdelete"))
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
                f"🤖 ʙᴏᴛ @{cloned_bot['username']} ʜᴀꜱ ʙᴇᴇɴ ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ ᴅᴇʟᴇᴛᴇᴅ ꜰʀᴏᴍ ᴅᴀᴛᴀʙᴀꜱᴇ."
            )
        else:
            await ok.edit_text("⚠️ ᴛʜᴇ ᴘʀᴏᴠɪᴅᴇᴅ ʙᴏᴛ ᴛᴏᴋᴇɴ ɪꜱ ɴᴏᴛ ɪɴ ᴛʜᴇ ᴄʟᴏɴᴇᴅ ʟɪꜱᴛ.")
    except Exception as e:
        logging.exception(e)
        await message.reply_text(f"Error occurred: {e}")

@bot.on_message(filters.command(["deleteall"]) & filters.user(SUDOERS))
async def delete_all_cloned_bots(client, message):
    try:
        a = await message.reply_text("ᴅᴇʟᴇᴛɪɴɢ ᴀʟʟ ᴄʟᴏɴᴇᴅ ʙᴏᴛꜱ...")
        await clonebotdb.delete_many({})
        CLONES.clear()
        await a.edit_text("ᴀʟʟ ᴄʟᴏɴᴇᴅ ʙᴏᴛꜱ ʜᴀᴠᴇ ʙᴇᴇɴ ꜱᴜᴄᴄᴇꜱꜰᴜʟʟʏ ᴅᴇʟᴇᴛᴇᴅ ✅")
    except Exception as e:
        logging.exception(e)
        await message.reply_text(f"Error occurred while deleting all cloned bots: {e}")

@bot.on_message(filters.command("updateall") & filters.user(SUDOERS))
async def update_all_bots(client, message):
    try:
        a = await message.reply_text("🔄 Updating all bots from the repository...")
        process = subprocess.run(["git", "pull"], capture_output=True, text=True)
        if process.returncode == 0:
            await a.edit_text("✅ All bots have been updated successfully!")
        else:
            await a.edit_text(f"⚠️ Update failed:\n\n{process.stderr}")
    except Exception as e:
        logging.exception(e)
        await message.reply_text(f"Error occurred during update: {e}")
        
@bot.on_message(filters.command("botdelete"))
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
                f"🤖 Your cloned bot **@{cloned_bot['username']}** has been removed from my database ✅.\n"
                "🔄 Kindly revoke your bot token from @BotFather for security purposes."
            )
        else:
            await ok.edit_text("⚠️ The provided bot token is not in the cloned list.")
    except Exception as e:
        logging.exception(e)
        await message.reply_text(f"An error occurred while deleting the cloned bot: {e}")
        
        
@bot.on_message(filters.command("botlist"))
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
