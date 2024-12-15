import asyncio
from pyrogram import filters, Client
from pyrogram.types import Message
from BADUC import SUDOERS
from BADUC.core.clients import app
from BADUC.core.command import *


@app.on_message(bad(["lyrics"]) & (filters.me | filters.user(SUDOERS)))
async def send_lyrics(bot: Client, message: Message):
    try:
        cmd = message.command
        song_name = ""

        if len(cmd) > 1:
            song_name = " ".join(cmd[1:])
        elif message.reply_to_message:
            if message.reply_to_message.audio:
                song_name = f"{message.reply_to_message.audio.title} {message.reply_to_message.audio.performer}"
            elif message.reply_to_message.text:
                song_name = message.reply_to_message.text
        elif not message.reply_to_message and len(cmd) == 1:
            await message.edit("Please provide a song name.")
            await asyncio.sleep(2)
            await message.delete()
            return

        await message.edit(f"Searching lyrics for `{song_name}`...")

        try:
            # Attempt to get inline bot results
            lyrics_results = await bot.get_inline_bot_results("ilyricsbot", song_name)

            if not lyrics_results.results:
                await message.edit("No lyrics found.")
                await asyncio.sleep(2)
                await message.delete()
                return

            # Send to saved messages because 'hide_via' may fail
            saved = await bot.send_inline_bot_result(
                chat_id="me",
                query_id=lyrics_results.query_id,
                result_id=lyrics_results.results[0].id,
            )
            await asyncio.sleep(2)

            # Forward the result to the original chat
            await bot.copy_message(
                chat_id=message.chat.id,
                from_chat_id="me",
                message_id=saved.updates[1].message.id,
            )

            # Delete the message from saved messages after forwarding
            await bot.delete_messages("me", saved.updates[1].message.id)

        except TimeoutError:
            await message.edit("Sorry, something went wrong while fetching the lyrics.")
            await asyncio.sleep(2)

        await message.delete()

    except Exception as e:
        await message.edit(f"`Failed to find lyrics: {str(e)}`")
        await asyncio.sleep(2)
        await message.delete()


__NAME__ = "Lʏʀɪᴄs"
__MENU__ = """
`.l` - **Search lyrics and send..**
"""
