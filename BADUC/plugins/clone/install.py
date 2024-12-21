import importlib
import os
import sys
from pathlib import Path

from BADUC import SUDOERS
from BADUC.core.command import *

from pyrogram import Client, filters
from pyrogram.types import Message

# Create a folder for plugins if it doesn't exist
os.makedirs("BADUC/plugins/clone", exist_ok=True)


@Client.on_message(bad(["install"]) & (filters.me | filters.user(SUDOERS)))
async def install_plugins(client: Client, message: Message):
    if not message.reply_to_message or not message.reply_to_message.document:
        return await message.reply_text("Reply to a plugin file to install it.", quote=True)

    msg = await message.reply_text("**Installing...**", quote=True)
    plugin_path = await message.reply_to_message.download("BADUC/plugins/clone/")

    if not plugin_path.endswith(".py"):
        os.remove(plugin_path)
        return await msg.edit("**Invalid Plugin:** Not a Python file.")

    plugin_name = Path(plugin_path).stem
    try:
        spec = importlib.util.spec_from_file_location(plugin_name, plugin_path)
        load = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(load)
        sys.modules[f"plugins.{plugin_name}"] = load
        await msg.edit(f"**Installed Successfully:** `{plugin_name}.py`")
    except Exception as e:
        await msg.edit(f"**Error:** {str(e)}")
        os.remove(plugin_path)


@Client.on_message(bad(["uninstall"]) & (filters.me | filters.user(SUDOERS)))
async def uninstall_plugins(client: Client, message: Message):
    if len(message.command) < 2:
        return await message.reply_text("Provide the plugin name to uninstall.", quote=True)

    plugin_name = message.command[1].strip().replace(".py", "")
    plugin_path = f"BADUC/plugins/clone/{plugin_name}.py"

    if not os.path.exists(plugin_path):
        return await message.reply_text(f"**Plugin Not Found:** `{plugin_name}`", quote=True)

    try:
        os.remove(plugin_path)
        sys.modules.pop(f"plugins.{plugin_name}", None)
        await message.reply_text(f"**Uninstalled Successfully:** `{plugin_name}.py`", quote=True)
    except Exception as e:
        await message.reply_text(f"**Error:** {str(e)}", quote=True)
      
