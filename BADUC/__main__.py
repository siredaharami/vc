import asyncio, importlib

from pytgcalls import idle

from BADUC.core.scan import logs, plugs, vars
from BADUC.plugins import ALL_PLUGINS
from BADUC.core.clients import run_async_clients
from BADUC.functions.enums import run_async_enums
from BADUC.database.test import *

async def main():
    await run_async_clients()
    for all_plugin in ALL_PLUGINS:
        imported_plugin = importlib.import_module(
            "BADUC.plugins" + all_plugin
        )
        if (hasattr
            (
                imported_plugin, "__NAME__"
            ) and imported_plugin.__NAME__
        ):
            imported_plugin.__NAME__ = imported_plugin.__NAME__
            if (
                hasattr(
                    imported_plugin, "__MENU__"
                ) and imported_plugin.__MENU__
            ):
                plugs[imported_plugin.__NAME__.lower()
                ] = imported_plugin
    await run_async_enums()
    logs.info(">> Successfully Imported All Plugins.")
    await run_async_inline()
    logs.info("Successfully Deployed !!")
    logs.info("Do Visit - @PBX_CHAT")
    await idle()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    print("Userbot Stopped !\nGoodBye ...")
