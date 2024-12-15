import traceback
import subprocess
from pyrogram import Client, filters
from pyrogram.types import Message
import aiohttp, aiofiles, asyncio, base64, logging
import os, platform, random, re, socket
import sys, time, textwrap
from os import getenv
from io import BytesIO
from time import strftime
from functools import partial
from dotenv import load_dotenv
from datetime import datetime

from BADUC import SUDOERS
from BADUC.core.clients import app
from BADUC.core.command import *

from typing import Union, List, Pattern
from git import Repo
from git.exc import GitCommandError, InvalidGitRepositoryError

async def edit_or_reply(msg: Message, **kwargs):
    func = msg.edit_text if msg.from_user.is_self else msg.reply
    await func(**kwargs)

@app.on_message(bad(["gitpull", "update"]) & (filters.me | filters.user(SUDOERS)))
async def update_repo_latest(client, message):
    response = await message.reply_text("Checking for available updates...")
    try:
        repo = Repo()
    except GitCommandError:
        await response.edit("Git Command Error")
        await message.delete()  # Delete the command message
        return
    except InvalidGitRepositoryError:
        await response.edit("Invalid Git Repository")
        await message.delete()  # Delete the command message
        return
    
    to_exc = f"git fetch origin main &> /dev/null"
    os.system(to_exc)
    await asyncio.sleep(7)
    verification = ""
    REPO_ = repo.remotes.origin.url.split(".git")[0]  # main git repository
    for checks in repo.iter_commits(f"HEAD..origin/main"):
        verification = str(checks.count())
    if verification == "":
        await response.edit("userbot is up-to-date!")
        await message.delete()  # Delete the command message
        return

    updates = ""
    ordinal = lambda format: "%d%s" % (
        format,
        "tsnrhtdd"[(format // 10 % 10 != 1) * (format % 10 < 4) * format % 10 :: 4],
    )
    for info in repo.iter_commits(f"HEAD..origin/main"):
        updates += f"<b>➣ #{info.count()}: [{info.summary}]({REPO_}/commit/{info}) by -> {info.author}</b>\n\t\t\t\t<b>➥ Committed on:</b> {ordinal(int(datetime.fromtimestamp(info.committed_date).strftime('%d')))} {datetime.fromtimestamp(info.committed_date).strftime('%b')}, {datetime.fromtimestamp(info.committed_date).strftime('%Y')}\n\n"
    
    _update_response_ = "<b>A new update is available for the userbot!</b>\n\n➣ Pushing Updates Now</code>\n\n**<u>Updates:</u>**\n\n"
    _final_updates_ = _update_response_ + updates
    if len(_final_updates_) > 4096:
        link = await paste_queue(updates)
        url = link + "/index.txt"
        nrs = await response.edit(
            f"<b>A new update is available for the userbot!</b>\n\n➣ Pushing Updates Now</code>\n\n**<u>Updates:</u>**\n\n[Click Here to check out Updates]({url})"
        )
    else:
        nrs = await response.edit(_final_updates_, disable_web_page_preview=True)
    
    os.system("git stash &> /dev/null && git pull")
    await response.edit(
        f"{nrs.text}\n\nuserbot was updated successfully! Now, wait for 1 - 2 mins until the userbot reboots!"
    )
    
    os.system("pip3 install -r requirements.txt --force-reinstall")
    os.system(f"kill -9 {os.getpid()} && python3 -m BADUC")
    sys.exit()
    
    await message.delete()  # Delete the command message after processing

@app.on_message(bad(["sh"]) & (filters.me | filters.user(SUDOERS)))
async def shellrunner(_, message: Message):
    if len(message.command) < 2:
        return await edit_or_reply(message, text="<b>ᴇxᴀᴍᴩʟᴇ :</b>\n/sh git pull")
    
    text = message.text.split(None, 1)[1]
    if "\n" in text:
        code = text.split("\n")
        output = ""
        for x in code:
            shell = re.split(""" (?=(?:[^'"]|'[^']*'|"[^"]*")*$)""", x)
            try:
                process = subprocess.Popen(
                    shell,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                )
            except Exception as err:
                await edit_or_reply(message, text=f"<b>ERROR :</b>\n<pre>{err}</pre>")
                await message.delete()  # Delete the command message if an error occurs
                return
            output += f"<b>{x}</b>\n"
            output += process.stdout.read()[:-1].decode("utf-8")
            output += "\n"
    else:
        shell = re.split(""" (?=(?:[^'"]|'[^']*'|"[^"]*")*$)""", text)
        for a in range(len(shell)):
            shell[a] = shell[a].replace('"', "")
        try:
            process = subprocess.Popen(
                shell,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
        except Exception as err:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            errors = traceback.format_exception(exc_type, exc_obj, exc_tb)
            await edit_or_reply(
                message, text=f"<b>ERROR :</b>\n<pre>{''.join(errors)}</pre>"
            )
            await message.delete()  # Delete the command message after error
            return
        output = process.stdout.read()[:-1].decode("utf-8")
    
    if str(output) == "\n":
        output = None
    
    if output:
        if len(output) > 4096:
            with open("output.txt", "w+") as file:
                file.write(output)
            await app.send_document(
                message.chat.id,
                "output.txt",
                reply_to_message_id=message.id,
                caption="<code>Output</code>",
            )
            os.remove("output.txt")
        else:
            await edit_or_reply(message, text=f"<b>OUTPUT :</b>\n<pre>{output}</pre>")
    else:
        await edit_or_reply(message, text="<b>OUTPUT :</b>\n<code>None</code>")
    
    await message.delete()  # Delete the command message after processing

__NAME__ = " Aᴅᴍɪɴ "
__MENU__ = """
`.ban` **ban user**
`.unban` **unban user**
`.mute` **mute user**
`.unmute` **unmute user**
`.tmute` **timed mute user**
"""
