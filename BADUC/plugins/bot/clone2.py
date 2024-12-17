from BADUC.core.clients import *
from BADUC.core.config import *
from BADUC.core.command import *
from pyrogram import filters, Client, idle
from pyrogram.types import Message
import os
import json
import shutil

# Directory to store clone data
CLONE_DATA_FILE = "clone_data.json"
PLUGINS_DIR = "BADUC/plugins/clone2"

# Helper function to load clone data
def load_clone_data():
    if os.path.exists(CLONE_DATA_FILE):
        with open(CLONE_DATA_FILE, "r") as file:
            return json.load(file)
    return {}

# Helper function to save clone data
def save_clone_data(data):
    with open(CLONE_DATA_FILE, "w") as file:
        json.dump(data, file)

# Ensure the plugin directory exists
def ensure_plugin_directory():
    if not os.path.exists(PLUGINS_DIR):
        os.makedirs(PLUGINS_DIR)

# Function to copy plugins into the clone directory
def copy_plugins():
    source_plugin_dir = "BADUC/plugins/clone2"
    for plugin in os.listdir(source_plugin_dir):
        src_path = os.path.join(source_plugin_dir, plugin)
        dst_path = os.path.join(PLUGINS_DIR, plugin)
        if os.path.isdir(src_path) and not os.path.exists(dst_path):
            shutil.copytree(src_path, dst_path)

@bot.on_message(filters.command("clonee"))
async def clone(bot: Client, msg: Message):
    """
    Clone command: Clone a bot account using a provided bot token,
    load plugins for the cloned session, and store session info.
    """
    if len(msg.command) < 2:
        await msg.reply("Usage: `/clone <bot_token>`\nSend your bot token to clone. 🤖")
        return

    bot_token = msg.command[1]
    clone_data = load_clone_data()

    if bot_token in clone_data:
        await msg.reply("This bot has already been cloned!")
        return
    
    try:
        reply_msg = await msg.reply("Please wait... Setting up the bot and loading plugins. 🔄")

        # Ensure plugin directory
        ensure_plugin_directory()
        copy_plugins()

        # Initialize bot client
        client = Client(
            name="ClonedBot",
            api_id=API_ID,       # Add API ID here
            api_hash=API_HASH,   # Add API Hash here
            bot_token=bot_token,
            plugins=dict(root=PLUGINS_DIR)
        )

        # Start client and fetch bot details
        await client.start()
        bot_info = await client.get_me()

        # Save bot clone info
        clone_data[bot_token] = {
            "bot_id": bot_info.id,
            "bot_username": bot_info.username,
            "plugins": os.listdir(PLUGINS_DIR)
        }
        save_clone_data(clone_data)

        # Notify owner
        owner_msg = f"New bot clone created:\n\n" \
                    f"**Bot Username:** @{bot_info.username}\n" \
                    f"**Bot ID:** {bot_info.id}\n" \
                    f"**Plugins:** {', '.join(os.listdir(PLUGINS_DIR))}"
        await bot.send_message(OWNER_ID, owner_msg)

        # Success message
        success_msg = (
            f"✅ Bot cloned successfully!\n\n"
            f"🤖 **Bot Username:** @{bot_info.username}\n"
            f"🆔 **Bot ID:** {bot_info.id}\n"
            f"**Plugins Loaded:** {', '.join(os.listdir(PLUGINS_DIR))}"
        )
        await reply_msg.edit(success_msg)

        # Keep bot running
        print("Cloned bot session running. Press Ctrl+C to stop.")
        await idle()

    except Exception as e:
        error_msg = f"❌ **ERROR:** `{str(e)}`\nPlease check your bot token, API ID, or API Hash."
        await msg.reply(error_msg)
    finally:
        if client.is_connected:
            await client.stop()

@bot.on_message(filters.command("list"))
async def clone_list(bot: Client, msg: Message):
    clone_data = load_clone_data()
    if not clone_data:
        await msg.reply("No bot clones available.")
        return
    
    clone_list_msg = "Cloned Bots:\n\n"
    for token, details in clone_data.items():
        clone_list_msg += f"**Bot Username:** @{details['bot_username']} | **Bot ID:** {details['bot_id']} | **Plugins:** {', '.join(details['plugins'])}\n"
    
    await msg.reply(clone_list_msg)

@bot.on_message(filters.command("delete"))
@super_user_only
async def clone_delete(bot: Client, msg: Message):
    if len(msg.command) < 2:
        await msg.reply("Usage: `/delete <bot_token>`\nProvide the bot token to delete.")
        return
    
    bot_token = msg.command[1]
    clone_data = load_clone_data()

    if bot_token not in clone_data:
        await msg.reply("Bot clone not found!")
        return
    
    del clone_data[bot_token]
    save_clone_data(clone_data)

    await msg.reply(f"Cloned bot with token `{bot_token}` has been deleted.")
    await bot.send_message(OWNER_ID, f"Bot clone deleted: `{bot_token}`")
