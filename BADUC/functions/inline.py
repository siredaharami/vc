import asyncio
from . import *
from BADUC.functions.button import *
from BADUC.functions.text import *
from pyrogram.types import *


async def help_menu_logo(answer):
    # Providing a fallback thumbnail image directly
    thumb_image = "https://files.catbox.moe/83d5lc.jpg"
    
    # Check if `image` exists and assign it
    image = None  # Replace this with logic to fetch `image` dynamically
    if image:
        thumb_image = image  # Use dynamic image if available
    
    # Count total plugins dynamically
    total_plugins = len(plugs) if 'plugs' in globals() else 0
    
    # Generate the button
    button = paginate_plugins(0, plugs, "help")
    
    # Append InlineQueryResultPhoto
    answer.append(
        InlineQueryResultPhoto(
            photo_url=thumb_image,
            title="👻 𝖧𝖾𝗅𝗉 𝖬𝖾𝗇𝗎 𝖿𝗈𝗋:**{message.from_user.first_name}**",
            thumb_url=thumb_image,
            description=f"📃 𝖫𝗈𝖺𝖽𝖾𝖽__ {total_plugins} 𝗉𝗅𝗎𝗀𝗂𝗇𝗌 📱",
            caption=f"""
            **💫 Bad-Userbot Help Menu 👻  » {__version__} ✨
            ❤️ᴛᴏᴛᴀʟ ᴘʟᴜɢɪɴꜱ: {total_plugins} ❤️***""",
            reply_markup=InlineKeyboardMarkup(button),
        )
    )
    return answer


async def help_menu_text(answer):
    # Importing `__version__` dynamically
    from ... import __version__
    
    # Count total plugins dynamically
    total_plugins = len(plugs) if 'plugs' in globals() else 0
    
    # Generate the button
    button = paginate_plugins(0, plugs, "help")
    
    # Append InlineQueryResultArticle
    answer.append(
        InlineQueryResultArticle(
            title=f"👻 𝖧𝖾𝗅𝗉 𝖬𝖾𝗇𝗎 𝖿𝗈𝗋:**{message.from_user.first_name}** 📃 𝖫𝗈𝖺𝖽𝖾𝖽__ {total_plugins})",
            input_message_content=InputTextMessageContent(
                f"""
                **💫 Bad-Userbot Help Menu 👻  » {__version__} ✨
            ❤️ᴛᴏᴛᴀʟ ᴘʟᴜɢɪɴꜱ: {total_plugins} ❤️***""",
                disable_web_page_preview=True,
            ),
            reply_markup=InlineKeyboardMarkup(button),
        )
    )
    return answer


async def run_async_inline():
    @bot.on_inline_query()
    @inline_wrapper
    async def inline_query_handler(bot, query):
        text = query.query
        
        try:
            # Process "help_menu_logo" query
            if text.startswith("help_menu_logo"):
                answer = []
                answer = await help_menu_logo(answer)
                await bot.answer_inline_query(query.id, results=answer, cache_time=10)
            
            # Process "help_menu_text" query
            elif text.startswith("help_menu_text"):
                answer = []
                answer = await help_menu_text(answer)
                await bot.answer_inline_query(query.id, results=answer, cache_time=10)
        
        except Exception as e:
            print(f"Error: {e}")
            return
