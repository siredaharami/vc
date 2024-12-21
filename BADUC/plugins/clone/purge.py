import asyncio

from pyrogram import Client
from pyrogram.types import Message
from pyrogram import Client, filters

from BADUC import SUDOERS
from BADUC.core.command import *


def _chunk(from_msg: int, to_msg: int):
    curr_msg = from_msg

    while curr_msg < to_msg:
        yield list(range(curr_msg, min(curr_msg + 100, to_msg)))
        curr_msg += 100


@Client.on_message(bad(["purge"]) & (filters.me | filters.user(SUDOERS)))
async def purgeMsg(client: Client, message: Message):
    if not message.reply_to_message:
        return await Client.delete(
            message, "__Reply to a message to delete all messages after that.__"
        )

    deleted = 0
    from_msg = message.reply_to_message

    Client = await Client.edit(message, "__Purging...__")
    for msg_ids in _chunk(from_msg.id, message.id + 1):
        try:
            status = await client.delete_messages(message.chat.id, msg_ids)
            deleted += status
        except:
            pass

    await Client.delete(Client, f"__🧹 Purged {deleted} messages.__")


@Client.on_message(bad(["purgeme"]) & (filters.me | filters.user(SUDOERS)))
async def purgeMe(client: Client, message: Message):
    if len(message.command) < 2:
        return await Client.delete(
            message, "__Give the number of messages you want to delete.__"
        )
    try:
        count = int(message.command[1])
    except:
        return await Client.delete(message, "Argument must be an integer.")

    Client = await Client.edit(message, "__Purging...__")
    async for msgs in client.search_messages(
        message.chat.id, limit=count, from_user="me"
    ):
        try:
            await msgs.delete()
        except:
            pass

    await Client.delete(Client, f"__🧹 Purged {count} messages.__")


@Client.on_message(bad(["purgeuser"]) & (filters.me | filters.user(SUDOERS)))
async def purgeUser(client: Client, message: Message):
    if not message.reply_to_message or not message.reply_to_message.from_user:
        return await Client.delete(
            message, "__Reply to a user to delete their messages.__"
        )

    count = 0
    if len(message.command) > 1:
        try:
            count = int(message.command[1])
        except:
            return await Client.delete(message, "Argument must be an integer.")

    Client = await Client.edit(message, "__Purging...__")
    async for msgs in client.search_messages(
        message.chat.id, limit=count, from_user=message.reply_to_message.from_user.id
    ):
        try:
            await msgs.delete()
        except:
            pass

    await Client.delete(
        Client,
        f"__🧹 Purged {count} messages of {message.reply_to_message.from_user.mention}.__,,"
    )


@Client.on_message(bad(["del"]) & (filters.me | filters.user(SUDOERS)))
async def delMsg(_, message: Message):
    if not message.reply_to_message:
        return await Client.delete(
            message, "__Reply to a message to delete that message.__"
        )

    await message.reply_to_message.delete()
    await message.delete()


@Client.on_message(bad(["sd"]) & (filters.me | filters.user(SUDOERS)))
async def selfdestruct(client: Client, message: Message):
    if len(message.command) < 3:
        return await Client.delete(
            message, "__Give the number of seconds and the message to self-destruct.__"
        )

    try:
        seconds = int(message.command[1])
    except:
        return await Client.delete(message, "Argument must be an integer.")

    msg = " ".join(message.command[2:])
    await message.delete()
    x = await client.send_message(message.chat.id, msg)
    await asyncio.sleep(seconds)
    await x.delete()

