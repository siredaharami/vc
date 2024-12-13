import asyncio, importlib

from pytgcalls import idle

from . import logs, plugs, vars
from .plugins import ALL_PLUGINS
from BADUC.core.clients import run_async_clients
from BADUC.functions.enums import run_async_enums
from BADUC.functions.inline import run_async_inline

import asyncio
import importlib
from pytgcalls import idle

from .core import logs, plugs, vars
from .plugins import ALL_PLUGINS
from .core.clients import run_async_clients
from .functions.enums import run_async_enums
from .functions.inline import run_async_inline


async def import_plugins():
    """Imports and registers all plugins while logging their names."""
    for plugin_name in ALL_PLUGINS:
        module_path = f"BADUC.plugins{plugin_name}"
        try:
            imported_plugin = importlib.import_module(module_path)

            # Check and log plugin name if it exists
            if getattr(imported_plugin, "__NAME__", None):
                plugin_name_lower = imported_plugin.__NAME__.lower()
                plugs[plugin_name_lower] = imported_plugin
                logs.info(f"Imported plugin: {imported_plugin.__NAME__}")

                # Additional log for plugins with a menu
                if getattr(imported_plugin, "__MENU__", None):
                    logs.info(f"Plugin with menu loaded: {imported_plugin.__NAME__}")
            else:
                logs.warning(f"Plugin {plugin_name} does not have a __NAME__ attribute.")

        except Exception as e:
            logs.error(f"Failed to import plugin {plugin_name}: {e}")


async def main():
    """Main asynchronous function to initialize the bot."""
    await run_async_clients()
    await import_plugins()
    await run_async_enums()
    logs.info(">> Successfully Imported All Plugins.")
    await run_async_inline()
    logs.info("Successfully Deployed!")
    logs.info("Do Visit - @PBX_CHAT")
    await idle()


if __name__ == "__main__":
    asyncio.run(main())
    print("Userbot Stopped! Goodbye...")
