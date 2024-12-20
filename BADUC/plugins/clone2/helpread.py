from pyrogram import Client
from BADUC.plugins.clone2.help import plugin  # Ensure the correct path for the decorator

# 1. banall Plugin
@plugin(
    name="banall",
    description="""
    **BanAll Plugin**
    - **Command**: /banall
    - **Description**: Bans all members from the group.
    - **Usage**: Type /banall to remove all members from the group.
    """
)
async def banall_plugin(client: Client, message):
    await message.reply_text("All members have been banned!")

# 2. replyraid Plugin
@plugin(
    name="replyraid",
    description="""
    **ReplyRaid Plugin**
    - **Commands**:
      - /hreplyraid: Start a high-intensity reply raid.
      - /preplyraid: Start a persistent reply raid.
      - /replyraid: Start a standard reply raid.
    - **Description**: This plugin triggers a raid-like series of replies to messages.
    - **Usage**: Type one of the above commands to start a reply raid.
    """
)
async def replyraid_plugin(client: Client, message):
    await message.reply_text("Reply raid initiated!")

# 3. ping Plugin
@plugin(
    name="ping",
    description="""
    **Ping Plugin**
    - **Command**: /ping
    - **Description**: Check the bot's responsiveness.
    - **Usage**: Type /ping to get a response time from the bot.
    """
)
async def ping_plugin(client: Client, message):
    await message.reply_text("Pong! The bot is active.")

# 4. tager Plugin
@plugin(
    name="tager",
    description="""
    **Tager Plugin**
    - **Commands**:
      - /utag: Tag users with a specific message.
      - /tagall: Tag all members in the group.
      - /ptag: Persistent tagging of users.
      - /pgntag: Tag users except admins.
      - /pgmtag: Tag group moderators.
      - /pvctag: Tag users in voice chat.
    - **Description**: This plugin provides tagging utilities for different scenarios.
    - **Usage**: Use the above commands based on the tagging needs.
    """
)
async def tager_plugin(client: Client, message):
    await message.reply_text("Tagging functionality accessed!")

# 5. raid Plugin
@plugin(
    name="raid",
    description="""
    **Raid Plugin**
    - **Commands**:
      - /hraid: Start a high-intensity raid.
      - /praid: Start a persistent raid.
      - /oneraid: Start a single-instance raid.
      - /raid: Start a general raid.
    - **Description**: This plugin triggers various types of raid events.
    - **Usage**: Use the above commands to trigger specific raids.
    """
)
async def raid_plugin(client: Client, message):
    await message.reply_text("Raid mode activated!")

# 6. spam Plugin
@plugin(
    name="spam",
    description="""
    **Spam Plugin**
    - **Commands**:
      - /emojiraid: Send a flood of emojis in the chat.
      - /mraid: Start a media spam raid.
    - **Description**: This plugin handles spamming functionalities for emojis and media.
    - **Usage**: Use the above commands for specific spamming needs.
    """
)
async def spam_plugin(client: Client, message):
    await message.reply_text("Spam functionality activated!")
