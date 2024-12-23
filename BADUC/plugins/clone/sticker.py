import imghdr
import math
import os
from asyncio import gather
from traceback import format_exc
from typing import List

from BADUC import SUDOERS
from BADUC.core.command import *

from PIL import Image
from pyrogram import Client, errors, filters, raw
from pyrogram.errors import (
    PeerIdInvalid,
    ShortnameOccupyFailed,
    StickerEmojiInvalid,
    StickerPngDimensions,
    StickerPngNopng,
    UserIsBlocked,
)
from pyrogram.file_id import FileId
from pyrogram.types import Message

MAX_STICKERS = (
    120  # would be better if we could fetch this limit directly from telegram
)
SUPPORTED_TYPES = ["jpeg", "png", "webp"]
STICKER_DIMENSIONS = (512, 512)


async def get_sticker_set_by_name(
    client: Client, name: str
) -> raw.base.messages.StickerSet:
    try:
        return await client.invoke(
            raw.functions.messages.GetStickerSet(
                stickerset=raw.types.InputStickerSetShortName(short_name=name),
                hash=0,
            )
        )
    except errors.exceptions.not_acceptable_406.StickersetInvalid:
        return None


async def create_sticker_set(
    client: Client,
    owner: int,
    title: str,
    short_name: str,
    stickers: List[raw.base.InputStickerSetItem],
) -> raw.base.messages.StickerSet:
    return await client.invoke(
        raw.functions.stickers.CreateStickerSet(
            user_id=await client.resolve_peer(owner),
            title=title,
            short_name=short_name,
            stickers=stickers,
        )
    )


async def add_sticker_to_set(
    client: Client,
    stickerset: raw.base.messages.StickerSet,
    sticker: raw.base.InputStickerSetItem,
) -> raw.base.messages.StickerSet:
    return await client.invoke(
        raw.functions.stickers.AddStickerToSet(
            stickerset=raw.types.InputStickerSetShortName(
                short_name=stickerset.set.short_name
            ),
            sticker=sticker,
        )
    )


async def create_sticker(
    sticker: raw.base.InputDocument, emoji: str
) -> raw.base.InputStickerSetItem:
    return raw.types.InputStickerSetItem(document=sticker, emoji=emoji)


async def resize_file_to_sticker_size(file_path: str) -> str:
    im = Image.open(file_path)
    if (im.width, im.height) < STICKER_DIMENSIONS:
        size1 = im.width
        size2 = im.height
        if im.width > im.height:
            scale = STICKER_DIMENSIONS[0] / size1
            size1new = STICKER_DIMENSIONS[0]
            size2new = size2 * scale
        else:
            scale = STICKER_DIMENSIONS[1] / size2
            size1new = size1 * scale
            size2new = STICKER_DIMENSIONS[1]
        size1new = math.floor(size1new)
        size2new = math.floor(size2new)
        sizenew = (size1new, size2new)
        im = im.resize(sizenew)
    else:
        im.thumbnail(STICKER_DIMENSIONS)
    try:
        os.remove(file_path)
        file_path = f"{file_path}.png"
        return file_path
    finally:
        im.save(file_path)


async def upload_document(
    client: Client, file_path: str, chat_id: int
) -> raw.base.InputDocument:
    media = await client.invoke(
        raw.functions.messages.UploadMedia(
            peer=await client.resolve_peer(chat_id),
            media=raw.types.InputMediaUploadedDocument(
                mime_type=client.guess_mime_type(file_path) or "application/zip",
                file=await client.save_file(file_path),
                attributes=[
                    raw.types.DocumentAttributeFilename(
                        file_name=os.path.basename(file_path)
                    )
                ],
            ),
        )
    )
    return raw.types.InputDocument(
        id=media.document.id,
        access_hash=media.document.access_hash,
        file_reference=media.document.file_reference,
    )


async def get_document_from_file_id(
    file_id: str,
) -> raw.base.InputDocument:
    decoded = FileId.decode(file_id)
    return raw.types.InputDocument(
        id=decoded.media_id,
        access_hash=decoded.access_hash,
        file_reference=decoded.file_reference,
    )


@Client.on_message(bad(["stickerid"]) & (filters.me | filters.user(SUDOERS)))
async def sticker_id(_, message: Message):
    reply = message.reply_to_message

    if not reply:
        return await message.reply("Reply to a sticker.")

    if not reply.sticker:
        return await message.reply("Reply to a sticker.")

    await message.reply_text(f"`{reply.sticker.file_id}`")


@Client.on_message(bad(["getsticker"]) & (filters.me | filters.user(SUDOERS)))
async def sticker_image(_, message: Message):
    r = message.reply_to_message

    if not r:
        return await message.reply("Reply to a sticker.")

    if not r.sticker:
        return await message.reply("Reply to a sticker.")

    m = await message.reply("Sending..")
    f = await r.download(f"{r.sticker.file_unique_id}.png")

    await gather(
        *[
            message.reply_photo(f),
            message.reply_document(f),
        ]
    )

    await m.delete()
    os.remove(f)


async def get_sticker_set_by_name(client: Client, name: str):
    try:
        return await client.invoke(
            raw.functions.messages.GetStickerSet(
                stickerset=raw.types.InputStickerSetShortName(short_name=name),
                hash=0,
            )
        )
    except errors.exceptions.not_acceptable_406.StickersetInvalid:
        # Return None if the sticker set is invalid
        return None


@Client.on_message(filters.command("kang"))
async def kang(client, message: Message):
    if not message.reply_to_message:
        return await message.reply_text("Reply to a sticker/image to kang it.")
    if not message.from_user:
        return await message.reply_text("You are an anonymous admin. I can't kang for you.")
    
    msg = await message.reply_text("Kanging Sticker...")

    # Extract emoji
    args = message.text.split()
    sticker_emoji = args[1] if len(args) > 1 else "🤔"

    # Process the sticker/image
    try:
        doc = message.reply_to_message.sticker or message.reply_to_message.photo
        if not doc:
            return await msg.edit("No sticker or image found to kang.")
        
        if message.reply_to_message.sticker:
            sticker = await create_sticker(
                await get_document_from_file_id(message.reply_to_message.sticker.file_id),
                sticker_emoji,
            )
        else:
            temp_file_path = await client.download_media(message.reply_to_message)
            temp_file_path = await resize_file_to_sticker_size(temp_file_path)
            sticker = await create_sticker(
                await upload_document(client, temp_file_path, message.chat.id),
                sticker_emoji,
            )
            os.remove(temp_file_path)

        # Sticker pack details
        pack_num = 0
        pack_name = f"f{message.from_user.id}_kangpack"
        pack_title = f"{message.from_user.first_name[:32]}'s Kang Pack"

        # Debug log for pack_name
        print(f"Attempting to fetch or create sticker pack: {pack_name}")

        # Try to find or create the sticker set
        try:
            stickerset = await get_sticker_set_by_name(client, pack_name)
        except errors.exceptions.internal_server_error_500.StickersetInvalid:
            print("Sticker pack not found or invalid. Creating a new one...")
            stickerset = None

        if not stickerset:
            print("Creating new sticker pack...")
            stickerset = await create_sticker_set(
                client, 
                message.from_user.id, 
                pack_title, 
                pack_name, 
                [sticker]
            )
        else:
            try:
                await add_sticker_to_set(client, stickerset, sticker)
            except errors.StickerEmojiInvalid:
                return await msg.edit("Invalid emoji provided.")
            except Exception as e:
                return await msg.edit(f"Failed to add sticker: {str(e)}")

        await msg.edit(f"Sticker added to pack!\nEmoji: {sticker_emoji}")
    
    except Exception as e:
        await msg.edit(f"An error occurred: {e}")
        print(format_exc())
      
