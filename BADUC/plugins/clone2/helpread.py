from pyrogram import Client
from BADUC.plugins.clone2.help import plugin  # Ensure the correct path for the decorator

# 1. banall Plugin
@plugin(
    name="ʙᴀɴᴀʟʟ",
    description="""
    ʙᴀɴᴀʟʟ ᴘʟᴜɢɪɴ
    - ᴄᴏᴍᴍᴀɴᴅ: /banall
    - ᴅᴇsᴄʀɪᴘᴛɪᴏɴ: ʙᴀɴs ᴀʟʟ ᴍᴇᴍʙᴇʀs ғʀᴏᴍ ᴛʜᴇ ɢʀᴏᴜᴘ.
    - ᴜsᴀɢᴇ: ᴛʏᴘᴇ /ʙᴀɴᴀʟʟ ᴛᴏ ʀᴇᴍᴏᴠᴇ ᴀʟʟ ᴍᴇᴍʙᴇʀs ғʀᴏᴍ ᴛʜᴇ ɢʀᴏᴜᴘ.
    """
)
async def banall_plugin(client: Client, message):
    await message.reply_text("ᴀʟʟ ᴍᴇᴍʙᴇʀs ʜᴀᴠᴇ ʙᴇᴇɴ ʙᴀɴɴᴇᴅ!")

# 2. replyraid Plugin
@plugin(
    name="ʀᴇᴘʟʏʀᴀɪᴅ",
    description="""
    ʀᴇᴘʟʏʀᴀɪᴅ ᴘʟᴜɢɪɴ
    - ᴄᴏᴍᴍᴀɴᴅs:
      - /hreplyraid : sᴛᴀʀᴛ ᴀ ʜɪɢʜ-ɪɴᴛᴇɴsɪᴛʏ ʀᴇᴘʟʏ ʀᴀɪᴅ.
      - /preplyraid : sᴛᴀʀᴛ ᴀ ᴘᴇʀsɪsᴛᴇɴᴛ ʀᴇᴘʟʏ ʀᴀɪᴅ.
      - /replyraid : sᴛᴀʀᴛ ᴀ sᴛᴀɴᴅᴀʀᴅ ʀᴇᴘʟʏ ʀᴀɪᴅ.
    - ᴅᴇsᴄʀɪᴘᴛɪᴏɴ: ᴛʜɪs ᴘʟᴜɢɪɴ ᴛʀɪɢɢᴇʀs ᴀ ʀᴀɪᴅ-ʟɪᴋᴇ sᴇʀɪᴇs ᴏғ ʀᴇᴘʟɪᴇs ᴛᴏ ᴍᴇssᴀɢᴇs.
    - ᴜsᴀɢᴇ: ᴛʏᴘᴇ ᴏɴᴇ ᴏғ ᴛʜᴇ ᴀʙᴏᴠᴇ ᴄᴏᴍᴍᴀɴᴅs ᴛᴏ sᴛᴀʀᴛ ᴀ ʀᴇᴘʟʏ ʀᴀɪᴅ.
    """
)
async def replyraid_plugin(client: Client, message):
    await message.reply_text("ʀᴇᴘʟʏ ʀᴀɪᴅ ɪɴɪᴛɪᴀᴛᴇᴅ!")

# 3. ping Plugin
@plugin(
    name="ᴘɪɴɢ",
    description="""
    ᴘɪɴɢ ᴘʟᴜɢɪɴ
    - ᴄᴏᴍᴍᴀɴᴅ: /ping 
    - ᴅᴇsᴄʀɪᴘᴛɪᴏɴ: ᴄʜᴇᴄᴋ ᴛʜᴇ ʙᴏᴛ's ʀᴇsᴘᴏɴsɪᴠᴇɴᴇss.
    - ᴜsᴀɢᴇ: ᴛʏᴘᴇ /ᴘɪɴɢ ᴛᴏ ɢᴇᴛ ᴀ ʀᴇsᴘᴏɴsᴇ ᴛɪᴍᴇ ғʀᴏᴍ ᴛʜᴇ ʙᴏᴛ.
    """
)
async def ping_plugin(client: Client, message):
    await message.reply_text("ᴘᴏɴɢ! ᴛʜᴇ ʙᴏᴛ ɪs ᴀᴄᴛɪᴠᴇ.")

# 4. tager Plugin
@plugin(
    name="ᴛᴀɢᴇʀ",
    description="""
    ᴛᴀɢᴇʀ ᴘʟᴜɢɪɴ
    - ᴄᴏᴍᴍᴀɴᴅs:
      - /utag : ᴛᴀɢ ᴜsᴇʀs ᴡɪᴛʜ ᴀ sᴘᴇᴄɪғɪᴄ ᴍᴇssᴀɢᴇ.
      - /admins :  ᴛᴏ ᴛᴀɢ ᴀʟʟ ᴀᴅᴍɪɴ's ɪɴ ʏᴏᴜʀ ɢʀᴏᴜᴘ
      - /cancel : ᴛᴏ sᴛᴏᴘ ʀᴜɴɴɪɴɢ ᴀɴʏ ᴛᴀɢ ᴘʀᴏᴄᴇss
      - /tagall : ᴛᴀɢ ᴀʟʟ ᴍᴇᴍʙᴇʀs ɪɴ ᴛʜᴇ ɢʀᴏᴜᴘ.
      - /ptag : ᴘʙɪ ᴛᴀɢɢɪɴɢ ᴏғ ᴜsᴇʀs.
      - /pgntag : ᴘʙɪɢɴ ᴛᴀɢ ᴜsᴇʀs ᴀᴅᴍɪɴs.
      - /pgmtag : ᴘʙɪɢᴍ ᴛᴀɢ ɢʀᴏᴜᴘ ᴍᴏᴅᴇʀᴀᴛᴏʀs.
    - ᴅᴇsᴄʀɪᴘᴛɪᴏɴ: ᴛʜɪs ᴘʟᴜɢɪɴ ᴘʀᴏᴠɪᴅᴇs ᴛᴀɢɢɪɴɢ ᴜᴛɪʟɪᴛɪᴇs ғᴏʀ ᴅɪғғᴇʀᴇɴᴛ sᴄᴇɴᴀʀɪᴏs.
    - ᴜsᴀɢᴇ: ᴜsᴇ ᴛʜᴇ ᴀʙᴏᴠᴇ ᴄᴏᴍᴍᴀɴᴅs ʙᴀsᴇᴅ ᴏɴ ᴛʜᴇ ᴛᴀɢɢɪɴɢ ɴᴇᴇᴅs.
    """
)
async def tager_plugin(client: Client, message):
    await message.reply_text("ᴛᴀɢɢɪɴɢ ғᴜɴᴄᴛɪᴏɴᴀʟɪᴛʏ ᴀᴄᴄᴇssᴇᴅ!")

# 5. raid Plugin
@plugin(
    name="ʀᴀɪᴅ",
    description="""
    ʀᴀɪᴅ ᴘʟᴜɢɪɴ
    - ᴄᴏᴍᴍᴀɴᴅs:
    - ᴀʟʟ ᴄᴏᴍᴍᴀɴᴅꜱ ᴜꜱᴇ [ ᴄᴏᴍᴀɴᴅɴᴀᴍᴇ ᴛʏᴘᴇ ɴᴜᴍʙᴇʀ. /ᴘʀᴀɪᴅ 30 ]
      - /hraid : sᴛᴀʀᴛ ᴀ ʜɪɴᴅɪ ʀᴀɪᴅ.
      - /praid : sᴛᴀʀᴛ ᴀ ᴘᴜɴᴊᴀʙɪ ʀᴀɪᴅ.
      - /oneraid : sᴛᴀʀᴛ ᴀ sɪɴɢʟᴇ-ɪɴsᴛᴀɴᴄᴇ ʀᴀɪᴅ.
      - /raid : sᴛᴀʀᴛ ᴀ  ʀᴀɪᴅ.
    - ᴅᴇsᴄʀɪᴘᴛɪᴏɴ: ᴛʜɪs ᴘʟᴜɢɪɴ ᴛʀɪɢɢᴇʀs ᴠᴀʀɪᴏᴜs ᴛʏᴘᴇs ᴏғ ʀᴀɪᴅ ᴇᴠᴇɴᴛs.
    - ᴜsᴀɢᴇ: ᴜsᴇ ᴛʜᴇ ᴀʙᴏᴠᴇ ᴄᴏᴍᴍᴀɴᴅs ᴛᴏ ᴛʀɪɢɢᴇʀ sᴘᴇᴄɪғɪᴄ ʀᴀɪᴅs.
    """
)
async def raid_plugin(client: Client, message):
    await message.reply_text("ʀᴀɪᴅ ᴍᴏᴅᴇ ᴀᴄᴛɪᴠᴀᴛᴇᴅ!")

# 6. spam Plugin
@plugin(
    name="ꜱᴘᴀᴍ",
    description="""
    sᴘᴀᴍ ᴘʟᴜɢɪɴ
    - ᴄᴏᴍᴍᴀɴᴅs:
      - /emojiraid : sᴇɴᴅ ᴀ ғʟᴏᴏᴅ ᴏғ ᴇᴍᴏᴊɪs ɪɴ ᴛʜᴇ ᴄʜᴀᴛ.
      - /mraid : sᴛᴀʀᴛ ᴀ ᴍᴇᴅɪᴀ sᴘᴀᴍ ʀᴀɪᴅ.
      - /porn : ᴘʟᴇᴀꜱᴇ ᴘʀᴏᴠɪᴅᴇ ᴀ ᴛɪᴛʟᴇ ᴛᴏ ꜱᴇᴀʀᴄʜ
    - ᴅᴇsᴄʀɪᴘᴛɪᴏɴ: ᴛʜɪs ᴘʟᴜɢɪɴ ʜᴀɴᴅʟᴇs sᴘᴀᴍᴍɪɴɢ ғᴜɴᴄᴛɪᴏɴᴀʟɪᴛɪᴇs ғᴏʀ ᴇᴍᴏᴊɪs ᴀɴᴅ ᴍᴇᴅɪᴀ.
    - ᴜsᴀɢᴇ: ᴜsᴇ ᴛʜᴇ ᴀʙᴏᴠᴇ ᴄᴏᴍᴍᴀɴᴅs ғᴏʀ sᴘᴇᴄɪғɪᴄ sᴘᴀᴍᴍɪɴɢ ɴᴇᴇᴅs.
    """
)
async def spam_plugin(client: Client, message):
    await message.reply_text("sᴘᴀᴍ ғᴜɴᴄᴛɪᴏɴᴀʟɪᴛʏ ᴀᴄᴛɪᴠᴀᴛᴇᴅ!")
