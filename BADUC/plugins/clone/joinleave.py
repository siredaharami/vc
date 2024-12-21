from pyrogram import Client, enums, filters
from pyrogram.types import Message

from BADUC import SUDOERS
from BADUC.core.command import *

# Join a chat by chat ID or username
@Client.on_message(bad(["joingc"]) & (filters.me | filters.user(SUDOERS)))
async def join_chat(client: Client, message: Message):
    target = message.command[1] if len(message.command) > 1 else message.chat.id
    response = await message.reply_text("`Processing...`")
    try:
        await client.join_chat(target)
        await response.edit(f"**Successfully joined chat:** `{target}`")
    except Exception as ex:
        await response.edit(f"**Error:** \n\n{str(ex)}")

# Leave a chat by chat ID or username
@Client.on_message(bad(["leavegc"]) & (filters.me | filters.user(SUDOERS)))
async def leave_chat(client: Client, message: Message):
    target = message.command[1] if len(message.command) > 1 else message.chat.id
    response = await message.reply_text("`Processing...`")
    try:
        await response.edit_text(f"{client.me.first_name} has left this group. Goodbye!")
        await client.leave_chat(target)
    except Exception as ex:
        await response.edit_text(f"**Error:** \n\n{str(ex)}")

# Leave all group and supergroup chats
@Client.on_message(bad(["leaveallgc"]) & (filters.me | filters.user(SUDOERS)))
async def leave_all_groups(client: Client, message: Message):
    response = await message.reply_text("`Leaving all group chats...`")
    success, failure = 0, 0
    async for dialog in client.get_dialogs():
        if dialog.chat.type in (enums.ChatType.GROUP, enums.ChatType.SUPERGROUP):
            try:
                await client.leave_chat(dialog.chat.id)
                success += 1
            except Exception:
                failure += 1
    await response.edit(
        f"**Successfully left {success} group(s), failed to leave {failure} group(s).**"
    )

# Leave all channel chats
@Client.on_message(bad(["leaveallch"]) & (filters.me | filters.user(SUDOERS)))
async def leave_all_channels(client: Client, message: Message):
    response = await message.reply_text("`Leaving all channel chats...`")
    success, failure = 0, 0
    async for dialog in client.get_dialogs():
        if dialog.chat.type == enums.ChatType.CHANNEL:
            try:
                await client.leave_chat(dialog.chat.id)
                success += 1
            except Exception:
                failure += 1
    await response.edit(
        f"**Successfully left {success} channel(s), failed to leave {failure} channel(s).**"
    )
  
