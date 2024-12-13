import re
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from BADUC import __version__
from BADUC.core.clients import *
from BADUC.core.config import *
from BADUC.core.command import *
from BADUC.functions.button import *
from BADUC.functions.inline import *
from BADUC.functions.wrapper import *


@app.on_message(filters.command("help") & filters.user(sudo_users))
async def inline_help_menu(client, message):
    try:
        bot_results = await client.get_inline_bot_results(
            bot.me.username, "help_menu_text"
        )
        await client.send_inline_bot_result(
            chat_id=message.chat.id,
            query_id=bot_results.query_id,
            result_id=bot_results.results[0].id,
        )
        await message.delete()
    except Exception as e:
        print(f"Error in help menu: {e}")


@bot.on_callback_query(filters.regex(r"help_(.*?)"))
async def help_button(client, query):
    try:
        plug_match = re.match(r"help_plugin(.+?)", query.data)
        prev_match = re.match(r"help_prev(.+?)", query.data)
        next_match = re.match(r"help_next(.+?)", query.data)
        back_match = re.match(r"help_back", query.data)
        
        top_text = f"""
**💫 Welcome to the Help Menu!**
**Shukla Userbot - Version {__version__}**
Click on the buttons below to explore commands.
Powered by [Update](https://t.me/SHIVANSH474)
"""
        if plug_match:
            plugin = plug_match.group(1)
            text = f"**💫 Plugin: {plugin}**\n\n{plugs[plugin].__MENU__}"
            key = InlineKeyboardMarkup(
                [[InlineKeyboardButton("↪️ Back", callback_data="help_back")]]
            )
            await query.message.edit_text(
                text=text,
                reply_markup=key,
                disable_web_page_preview=True
            )
        elif prev_match:
            curr_page = int(prev_match.group(1))
            await query.message.edit_text(
                text=top_text,
                reply_markup=InlineKeyboardMarkup(
                    paginate_plugins(curr_page - 1, plugs, "help")
                ),
                disable_web_page_preview=True,
            )
        elif next_match:
            next_page = int(next_match.group(1))
            await query.message.edit_text(
                text=top_text,
                reply_markup=InlineKeyboardMarkup(
                    paginate_plugins(next_page + 1, plugs, "help")
                ),
                disable_web_page_preview=True,
            )
        elif back_match:
            await query.message.edit_text(
                text=top_text,
                reply_markup=InlineKeyboardMarkup(
                    paginate_plugins(0, plugs, "help")
                ),
                disable_web_page_preview=True,
            )
    except Exception as e:
        print(f"Error in help button: {e}")
