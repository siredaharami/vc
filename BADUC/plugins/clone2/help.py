from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, InputMediaPhoto
from BADUC.plugins.bot.clone3 import get_bot_owner  # Ensure correct import

# Dictionary to store plugin details automatically
plugin_details = {}

# Global variable to keep track of the current plugin being viewed
current_plugin_index = {}

# Decorator to register plugins automatically
def plugin(name, description):
    def decorator(func):
        plugin_details[name] = description
        return func
    return decorator

# Help command to show plugins with buttons and photo
@Client.on_message(filters.command("help"))
async def help(client: Client, message: Message, from_menu=False):
    bot_info = await client.get_me()  # Retrieve current bot's details
    bot_id = bot_info.id  # Get the current bot's ID
    user_id = message.from_user.id  # Get the user's ID

    if not from_menu:  # Skip authorization if called from the "Menu" button
        owner_id = await get_bot_owner(bot_id)
        if owner_id != user_id:
            await message.reply_text("❌ You're not authorized to access the help menu.")
            return

    # Define the photo URL (You can replace this with your desired image URL)
    photo_url = "https://files.catbox.moe/83d5lc.jpg"

    # Generate buttons for plugins
    buttons = []
    plugin_list = list(plugin_details.keys())

    for i in range(0, len(plugin_list), 2):
        row = []
        for j in range(2):
            if i + j < len(plugin_list):
                plugin_name = plugin_list[i + j]
                row.append(InlineKeyboardButton(f"{i + j + 1}. {plugin_name}", callback_data=f"plugin_{i + j + 1}"))
        buttons.append(row)

    # Add permanent "Support" and "Update" buttons
    buttons.append([
        InlineKeyboardButton("🥀 ꜱᴜᴘᴘᴏʀᴛ ❤️", url="https://t.me/PBX_CHAT"),
        InlineKeyboardButton("🥀 ᴜᴘᴅᴀᴛᴇ ❤️", url="https://t.me/HEROKUBIN_01")
    ])

    # Send the help menu
    if from_menu:
        await message.edit_media(
            media=InputMediaPhoto(photo_url, caption="👻 ʜᴇʟᴘ ᴍᴇɴᴜ ʙᴀᴅᴜꜱᴇʀ ʙᴏᴛ ❤️\n🔍ꜱᴇʟᴇᴄᴛ ᴀ ᴘʟᴜɢɪɴ ᴛᴏ ꜱᴇᴇ ɪᴛꜱ ᴅᴇᴛᴀɪʟꜱ📂"),
            reply_markup=InlineKeyboardMarkup(buttons)
        )
    else:
        await message.reply_photo(
            photo_url,
            caption="👻 ʜᴇʟᴘ ᴍᴇɴᴜ ʙᴀᴅᴜꜱᴇʀ ʙᴏᴛ ❤️\n🔍ꜱᴇʟᴇᴄᴛ ᴀ ᴘʟᴜɢɪɴ ᴛᴏ ꜱᴇᴇ ɪᴛꜱ ᴅᴇᴛᴀɪʟꜱ📂",
            reply_markup=InlineKeyboardMarkup(buttons)
        )

# Callback handler for buttons
@Client.on_callback_query()
async def button_handler(client, callback_query):
    global current_plugin_index
    user_id = callback_query.from_user.id
    data = callback_query.data

    if data.startswith("plugin_"):
        # Handle plugin details
        plugin_number = int(data.split("_")[1])
        plugin_name = list(plugin_details.keys())[plugin_number - 1]
        plugin_description = plugin_details[plugin_name]
        current_plugin_index[user_id] = plugin_number

        # Show plugin description with navigation buttons
        formatted_description = f"**ᴄᴏᴍᴍᴀɴᴅ:** {plugin_name}\n{plugin_description}"
        
        await callback_query.message.edit(
            text=formatted_description,
            reply_markup=InlineKeyboardMarkup([
                [
                    InlineKeyboardButton("↩️ ᴘʀᴇᴠɪᴏᴜꜱ", callback_data="prev"),
                    InlineKeyboardButton("ɴᴇxᴛ ↪️", callback_data="next")
                ],
                [InlineKeyboardButton("🔙 ᴍᴇɴᴜ", callback_data="menu")]
            ])
        )

    elif data == "next":
        # Handle "Next" button
        if user_id in current_plugin_index and current_plugin_index[user_id] < len(plugin_details):
            current_plugin_index[user_id] += 1
            plugin_number = current_plugin_index[user_id]
            plugin_name = list(plugin_details.keys())[plugin_number - 1]
            plugin_description = plugin_details[plugin_name]

            formatted_description = f"**ᴄᴏᴍᴍᴀɴᴅ:** {plugin_name}\n{plugin_description}"
            
            await callback_query.message.edit(
                text=formatted_description,
                reply_markup=InlineKeyboardMarkup([
                    [
                        InlineKeyboardButton("↩️ ᴘʀᴇᴠɪᴏᴜꜱ", callback_data="prev"),
                        InlineKeyboardButton("ɴᴇxᴛ ↪️", callback_data="next")
                    ],
                    [InlineKeyboardButton("🔙 ᴍᴇɴᴜ", callback_data="menu")]
                ])
            )

    elif data == "prev":
        # Handle "Previous" button
        if user_id in current_plugin_index and current_plugin_index[user_id] > 1:
            current_plugin_index[user_id] -= 1
            plugin_number = current_plugin_index[user_id]
            plugin_name = list(plugin_details.keys())[plugin_number - 1]
            plugin_description = plugin_details[plugin_name]

            formatted_description = f"**ᴄᴏᴍᴍᴀɴᴅ:** {plugin_name}\n{plugin_description}"
            
            await callback_query.message.edit(
                text=formatted_description,
                reply_markup=InlineKeyboardMarkup([
                    [
                        InlineKeyboardButton("↩️ ᴘʀᴇᴠɪᴏᴜꜱ", callback_data="prev"),
                        InlineKeyboardButton("ɴᴇxᴛ ↪️", callback_data="next")
                    ],
                    [InlineKeyboardButton("🔙 ᴍᴇɴᴜ", callback_data="menu")]
                ])
            )

    elif data == "menu":
        # Return to the main help menu
        await help(client, callback_query.message, from_menu=True)
