import asyncio
from re import sub
from threading import Event
from pyrogram import Client, enums, filters
from pyrogram.types import Message
from BADUC.database.data import GROUP
from BADUC.core.config import LOG_GROUP_ID
from BADUC.plugins.bot.clone3 import get_bot_owner  # Import the function to check bot owner
from time import time  # Used to implement cooldown functionality

commands = ["spam", "statspam", "slowspam", "fastspam"]
SPAM_COUNT = [0]
USER_LAST_COMMAND_TIME = {}  # Dictionary to store user command timestamps

# Maximum number of allowed spams per user (to prevent flooding)
MAX_SPAM_COUNT = 2999

# Cooldown time for commands (in seconds) to prevent rapid re-execution
COMMAND_COOLDOWN = 10 # 10 seconds cooldown between spam commands


def increment_spam_count():
    SPAM_COUNT[0] += 1
    return spam_allowed()


def spam_allowed():
    return SPAM_COUNT[0] < MAX_SPAM_COUNT


async def extract_args(message, markdown=True):
    if not (message.text or message.caption):
        return ""

    text = message.text or message.caption

    text = text.markdown if markdown else text
    if " " not in text:
        return ""

    text = sub(r"\s+", " ", text)
    text = text[text.find(" ") :].strip()
    return text


async def check_authorization(client, message):
    bot_info = await client.get_me()
    bot_id = bot_info.id
    user_id = message.from_user.id

    owner_id = await get_bot_owner(bot_id)
    if owner_id != user_id:
        await message.reply_text("❌ You're not authorized to use this bot.")
        return False
    return True


def is_command_on_cooldown(user_id):
    """Check if the user is within the cooldown period."""
    current_time = time()
    last_command_time = USER_LAST_COMMAND_TIME.get(user_id, 0)

    if current_time - last_command_time < COMMAND_COOLDOWN:
        return True
    return False


def update_last_command_time(user_id):
    """Update the time of the last executed command for the user."""
    USER_LAST_COMMAND_TIME[user_id] = time()


@Client.on_message(filters.command("dspam"))
async def delayspam(client: Client, message: Message):
    if not await check_authorization(client, message):
        return

    if is_command_on_cooldown(message.from_user.id):
        await message.reply_text("❌ You are on cooldown. Please wait a few seconds before using this command again.")
        return

    update_last_command_time(message.from_user.id)

    if message.chat.id in GROUP:
        return await message.reply_text(
            "**This command is not allowed to be used in this group**"
        )
    delayspam = await extract_args(message)
    arr = delayspam.split()
    delay = float(arr[0])
    count = int(arr[1])
    spam_message = delayspam.replace(arr[0], "", 1)
    spam_message = spam_message.replace(arr[1], "", 1).strip()
    await message.delete()

    if not spam_allowed():
        return

    delaySpamEvent = Event()
    for i in range(0, count):
        if i != 0:
            delaySpamEvent.wait(delay)
        await client.send_message(message.chat.id, spam_message)
        limit = increment_spam_count()
        if not limit:
            break

    await client.send_message(
        LOG_GROUP, "**#DELAYSPAM**\nDelaySpam was executed successfully"
    )


@Client.on_message(filters.command(commands, "/"))
async def sspam(client: Client, message: Message):
    if not await check_authorization(client, message):
        return

    if is_command_on_cooldown(message.from_user.id):
        await message.reply_text("❌ You are on cooldown. Please wait a few seconds before using this command again.")
        return

    update_last_command_time(message.from_user.id)

    if message.chat.id in GROUP:
        return await message.reply_text(
            "**This command is not allowed to be used in this group**"
        )
    amount = int(message.command[1])
    text = " ".join(message.command[2:])

    cooldown = {"spam": 0.1, "statspam": 0.1, "slowspam": 0.9, "fastspam": 0}

    await message.delete()

    for msg in range(amount):
        if message.reply_to_message:
            sent = await message.reply_to_message.reply(text)
        else:
            sent = await client.send_message(message.chat.id, text)

        if message.command[0] == "statspam":
            await asyncio.sleep(0.1)
            await sent.delete()

        await asyncio.sleep(cooldown[message.command[0]])


@Client.on_message(filters.command("sspam"))
async def spam_stick(client: Client, message: Message):
    if not await check_authorization(client, message):
        return

    if is_command_on_cooldown(message.from_user.id):
        await message.reply_text("❌ You are on cooldown. Please wait a few seconds before using this command again.")
        return

    update_last_command_time(message.from_user.id)

    if message.chat.id in GROUP:
        return await message.reply_text(
            "**This command is not allowed to be used in this group**"
        )
    if not message.reply_to_message:
        await message.reply_text(
            "**reply to a sticker with amount you want to spam**"
        )
        return
    if not message.reply_to_message.sticker:
        await message.reply_text(
            "**reply to a sticker with amount you want to spam**"
        )
        return
    else:
        i = 0
        times = message.command[1]
        if message.chat.type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
            for i in range(int(times)):
                sticker = message.reply_to_message.sticker.file_id
                await client.send_sticker(
                    message.chat.id,
                    sticker,
                )
                await asyncio.sleep(0.10)

        if message.chat.type == enums.ChatType.PRIVATE:
            for i in range(int(times)):
                sticker = message.reply_to_message.sticker.file_id
                await client.send_sticker(message.chat.id, sticker)
                await asyncio.sleep(0.10)
                
@Client.on_message(filters.command("mspam"))
async def mediaSpam(Client: Client, message: Message):
    # Authorization check
    if not await check_owner(Client, message):
        return

    if not message.reply_to_message:
        return await message.delete()

    if len(message.command) < 2:
        return await message.delete()

    try:
        count = int(message.command[1])
    except ValueError:
        await message.delete()
        return

    copy_id = message.reply_to_message.id
    event = asyncio.Event()
    task = asyncio.create_task(
        spam_text(Client, message.chat.id, None, count, None, None, copy_id, event)
    )

    if spamTask.get(message.chat.id, None):
        spamTask[message.chat.id].append(event)
    else:
        spamTask[message.chat.id] = [event]

    # Log spam initiation to the Logger Group
    await Client.send_message(
        LOG_GROUP_ID,
        f"**Spam Task Started**\n\n**Type:** Media Spam\n**Chat ID:** `{message.chat.id}`\n**Spam Count:** `{count}`",
    )

    await message.delete()
    await task
