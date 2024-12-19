import asyncio, importlib

from pytgcalls import idle

from . import logs, plugs, vars
from .plugins import ALL_PLUGINS
from BADUC import load_clone_owners
from BADUC.core.clients import run_async_clients
from BADUC.functions.enums import run_async_enums
from BADUC.functions.inline import run_async_inline


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
    await load_clone_owners()
    logs.info(">> Successfully Imported All Plugins.")
    await run_async_inline()
    logs.info("Successfully Deployed !!")
    logs.info("Do Visit - ")
    await idle()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    print("Userbot Stopped !\nGoodBye ...")
