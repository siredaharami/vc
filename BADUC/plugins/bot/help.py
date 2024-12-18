from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from CakeMusic import app

# Dictionary to store plugin details automatically
plugin_details = {}

# Global variable to keep track of the current plugin being viewed
current_plugin_index = {}

# Group and Owner Links
GROUP_LINK = "https://t.me/ll_BAD_MUNDA_WORLD_ll"
OWNER_LINK = "https://t.me/HEROKUBIN_01"

# Decorator to register plugins automatically
def plugin(name, description):
    def decorator(func):
        plugin_details[name] = description
        return func
    return decorator

# Command to show help with buttons
@app.on_message(filters.command("helhp"))
async def help(client: Client, message: Message):
    buttons = []
    plugin_list = list(plugin_details.keys())

    # Generate buttons for plugins
    for idx, plugin in enumerate(plugin_list, start=1):
        buttons.append([InlineKeyboardButton(f"{idx}. {plugin}", callback_data=f"plugin_{idx}")])

    # Add navigation buttons
    buttons.append([
        InlineKeyboardButton("👈 Previous", callback_data="prev"),
        InlineKeyboardButton("Next 👉", callback_data="next")
    ])
    buttons.append([
        InlineKeyboardButton("🔗 Group", url=GROUP_LINK),
        InlineKeyboardButton("👑 Owner", url=OWNER_LINK)
    ])

    # Send message with buttons
    await message.reply(
        "📚 **Help Menu** 📚\nSelect a plugin to see its details.",
        reply_markup=InlineKeyboardMarkup(buttons)
    )

# Callback handler for buttons
@app.on_callback_query()
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

        formatted_description = f"""```python
# Plugin Details:
# Command: {plugin_name}
{plugin_description}

# Group: {GROUP_LINK}
# Owner: {OWNER_LINK}
```"""
        await callback_query.message.edit(
            text=formatted_description,
            reply_markup=InlineKeyboardMarkup([
                [
                    InlineKeyboardButton("👈 Previous", callback_data="prev"),
                    InlineKeyboardButton("Next 👉", callback_data="next")
                ],
                [
                    InlineKeyboardButton("🔗 Group", url=GROUP_LINK),
                    InlineKeyboardButton("👑 Owner", url=OWNER_LINK)
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

            formatted_description = f"""```python
# Plugin Details:
# Command: {plugin_name}
{plugin_description}

# Group: {GROUP_LINK}
# Owner: {OWNER_LINK}
```"""
            await callback_query.message.edit(text=formatted_description)

    elif data == "prev":
        # Handle "Previous" button
        if user_id in current_plugin_index and current_plugin_index[user_id] > 1:
            current_plugin_index[user_id] -= 1
            plugin_number = current_plugin_index[user_id]
            plugin_name = list(plugin_details.keys())[plugin_number - 1]
            plugin_description = plugin_details[plugin_name]

            formatted_description = f"""```python
# Plugin Details:
# Command: {plugin_name}
{plugin_description}

# Group: {GROUP_LINK}
# Owner: {OWNER_LINK}
```"""
            await callback_query.message.edit(text=formatted_description)

# Example plugin added using the @plugin decorator
@app.on_message(filters.command("example"))
@plugin(
    name="example",
    description="""
**Example Plugin**
- **Command**: /example
- **Description**: This is an example plugin.
- **Usage**: Type /example to see the plugin in action.
"""
)
async def example(client: Client, message: Message):
    await message.reply("Example plugin is active!")
