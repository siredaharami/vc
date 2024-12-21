import os
import textwrap
from PIL import Image, ImageDraw, ImageFont
from pyrogram import filters
from pyrogram.types import Message
from BADUC import SUDOERS
from BADUC.core.command import *

@Client.on_message(bad(["mmf"]) & (filters.me | filters.user(SUDOERS)))
async def mmf(_, message: Message):
    chat_id = message.chat.id
    reply_message = message.reply_to_message

    if len(message.text.split()) < 2:
        await message.reply_text("❍ ʏᴏᴜ ᴍɪɢʜᴛ ᴡᴀɴᴛ ᴛᴏ ᴛʀʏ `/mmf ᴛᴇxᴛ`")
        await message.delete()
        return

    msg = await message.reply_text("❍ ᴍᴇᴍɪғʏɪɴɢ ᴛʜɪs ɪᴍᴀɢᴇ 🥀 ")
    text = message.text.split(None, 1)[1]
    
    if not reply_message or not reply_message.media:
        await msg.edit_text("❍ ᴘʟᴇᴀsᴇ ʀᴇᴘʟʏ ᴛᴏ ᴀɴ ɪᴍᴀɢᴇ.")
        await message.delete()
        return

    file = await Client.download_media(reply_message)

    try:
        meme = await drawText(file, text)
        if reply_message:
            await reply_message.reply_document(meme)
        else:
            await message.reply_document(meme)
    except Exception as e:
        await message.reply_text(f"❍ ᴇʀʀᴏʀ: {e}")
    finally:
        os.remove(meme)
        await msg.delete()
        await message.delete()


async def drawText(image_path, text):
    img = Image.open(image_path)
    os.remove(image_path)

    i_width, i_height = img.size

    if os.name == "nt":
        fnt = "arial.ttf"
    else:
        fnt = "./BADUC/resources/font/hiroko.ttf"

    m_font = ImageFont.truetype(fnt, int((70 / 640) * i_width))

    if ";" in text:
        upper_text, lower_text = text.split(";")
    else:
        upper_text = text
        lower_text = ""

    draw = ImageDraw.Draw(img)

    # Adjusted vertical position for text
    current_h, pad = int(20 / 640 * i_width), 5

    if upper_text:
        for u_text in textwrap.wrap(upper_text, width=15):
            u_width, u_height = draw.textsize(u_text, font=m_font)

            draw.text(
                xy=((i_width - u_width) / 2, current_h),
                text=u_text,
                font=m_font,
                fill=(255, 255, 255),
            )

            current_h += u_height + pad

    if lower_text:
        for l_text in textwrap.wrap(lower_text, width=15):
            l_width, l_height = draw.textsize(l_text, font=m_font)

            draw.text(
                xy=(
                    (i_width - l_width) / 2,
                    i_height - l_height - int(50 / 640 * i_width),
                ),
                text=l_text,
                font=m_font,
                fill=(255, 255, 255),
            )

            current_h += l_height + pad

    # Adding PNG overlay
    overlay_path = "./BADUC/resources/pic/overlay.png"  # Update the path to your PNG file
    if os.path.exists(overlay_path):
        overlay = Image.open(overlay_path).convert("RGBA")
        overlay = overlay.resize((i_width, int(i_height * 0.2)))  # Resize to fit
        img.paste(overlay, (0, i_height - overlay.size[1]), overlay)

    image_name = "memify.webp"
    webp_file = os.path.join(image_name)
    img.save(webp_file, "webp")

    return webp_file


__NAME__ = "Mᴍғ"
__MENU__ = """
`.mmf` - **Make a message into a sticker .**
"""
