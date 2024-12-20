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
async def help(client: Client, message: Message):
    bot_info = await client.get_me()  # Retrieve current bot's details
    bot_id = bot_info.id  # Get the current bot's ID
    user_id = message.from_user.id  # Get the user's ID

    # Check if the user is authorized to use this bot
    owner_id = await get_bot_owner(bot_id)
    if owner_id != user_id:
        await message.reply_text("❌ You're not authorized to access the help menu.")
        return

    # Define the photo URL (You can replace this with your desired image URL)
    photo_url = "https://files.catbox.moe/83d5lc.jpg"

    # Generate buttons for plugins
    buttons = []
    plugin_list = list(plugin_details.keys())

    for idx, plugin in enumerate(plugin_list, start=1):
        buttons.append([InlineKeyboardButton(f"{idx}. {plugin}", callback_data=f"plugin_{idx}")])

    # Add navigation buttons
    buttons.append([
        InlineKeyboardButton("↩️ ᴘʀᴇᴠɪᴏᴜꜱ", callback_data="prev"),
        InlineKeyboardButton("ɴᴇxᴛ ↪️", callback_data="next")
    ])

    # Send message with the photo and buttons
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

        # Send message with plugin description (no photo)
        formatted_description = f"**ᴄᴏᴍᴍᴀɴᴅ:** {plugin_name}\n{plugin_description}"
        
        await callback_query.message.edit(
            text=formatted_description,
            reply_markup=InlineKeyboardMarkup([
                [
                    InlineKeyboardButton("↩️ ᴘʀᴇᴠɪᴏᴜꜱ", callback_data="prev"),
                    InlineKeyboardButton("ɴᴇxᴛ ↪️", callback_data="next")
                ]
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
                    ]
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
                    ]
                ])
            )