import logging
import os
import asyncio
from pyrogram.enums import ParseMode
from pyrogram import Client, filters
from pyrogram.errors import PeerIdInvalid
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

async def get_bot_owner(bot_id):
    """
    Retrieve the owner of a specific bot.
    """
    owner = await cloneownerdb.find_one({"bot_id": bot_id})
    return owner["user_id"] if owner else None

def is_authorized(bot_id, user_id):
    """
    Check if the user is authorized to execute commands for a bot.
    """
    return CLONE_OWNERS.get(bot_id) == user_id

@bot.on_message(filters.command(["clone", "host", "deploy"]))
async def clone_txt(client, message):
    if len(message.command) > 1:
        bot_token = message.text.split("/clone", 1)[1].strip()
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

            try:
                # Notify the owner
                await client.send_message(
                    int(OWNER_ID), f"ɴᴇᴡ~ᴄʟᴏɴᴇ\n\nʙᴏᴛ:- @{bot.username}\n\nᴅᴇᴛᴀɪʟꜱ:-\n{details}"
                )
            except PeerIdInvalid:
                # Log the error if the bot hasn't met the owner
                await mi.edit_text("⚠️ Unable to notify the owner. Ensure the bot has interacted with the OWNER_ID user.")
                await ai.stop()
                return

            await clonebotdb.insert_one(details)
            CLONES.add(bot.id)

            await mi.edit_text(
                f"ʙᴏᴛ @{bot.username} ʜᴀꜱ ʙᴇᴇɴ ꜱᴜᴄᴄᴇꜱꜰᴜʟʟʏ ᴄʟᴏɴᴇᴅ."
            )
        except Exception as e:
            await mi.edit_text(f"[ʀᴏᴏᴛ]:: Error while cloning bot.\n\n**Error**: {e}")


