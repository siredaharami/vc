from pyrogram import Client
from BADUC.plugins.clone2.help import plugin  # Ensure the correct path for the decorator

# Define the admin plugin and its description
@plugin(
    name="admin",
    description="""
    **Admin Plugin**
    - **Command**: /admin
    - **Description**: This plugin gives admin-like controls, such as banning users or setting permissions.
    - **Usage**: Type /admin to access admin commands.
    """
)
async def admin_plugin(client: Client, message):
    # Example admin-related functionality
    await message.reply_text("Welcome to the admin panel!")
