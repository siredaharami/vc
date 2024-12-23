import asyncio
from functools import partial
from pyrogram import Client, filters
from pyrogram.types import Message
from pytgcalls import PyTgCalls
from BADUC.core.clients import *
import yt_dlp as ytdl  # We use yt-dlp to handle YouTube downloads and streaming
from pytgcalls.exceptions import NoActiveGroupCall
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pytgcalls.types import ChatUpdate, Update, GroupCallConfig
from pytgcalls.types import Call, MediaStream, AudioQuality, VideoQuality

# MongoDB Database Initialization (Assuming MongoDB is initialized elsewhere)
chatsdb = mongodb.chatsdb
usersdb = mongodb.usersdb


# Active chat and media management
ACTIVE_MEDIA_CHATS = []
ACTIVE_AUDIO_CHATS = []
ACTIVE_VIDEO_CHATS = []
QUEUE = {}

# Add active media chat
async def add_active_media_chat(chat_id, stream_type):
    if stream_type == "Audio":
        if chat_id in ACTIVE_VIDEO_CHATS:
            ACTIVE_VIDEO_CHATS.remove(chat_id)
        if chat_id not in ACTIVE_AUDIO_CHATS:
            ACTIVE_AUDIO_CHATS.append(chat_id)
    elif stream_type == "Video":
        if chat_id in ACTIVE_AUDIO_CHATS:
            ACTIVE_AUDIO_CHATS.remove(chat_id)
        if chat_id not in ACTIVE_VIDEO_CHATS:
            ACTIVE_VIDEO_CHATS.append(chat_id)
    if chat_id not in ACTIVE_MEDIA_CHATS:
        ACTIVE_MEDIA_CHATS.append(chat_id)

# Remove active media chat
async def remove_active_media_chat(chat_id):
    if chat_id in ACTIVE_AUDIO_CHATS:
        ACTIVE_AUDIO_CHATS.remove(chat_id)
    if chat_id in ACTIVE_VIDEO_CHATS:
        ACTIVE_VIDEO_CHATS.remove(chat_id)
    if chat_id in ACTIVE_MEDIA_CHATS:
        ACTIVE_MEDIA_CHATS.remove(chat_id)

# Check if a chat is served
async def is_served_chat(chat_id: int) -> bool:
    chat = await chatsdb.find_one({"chat_id": chat_id})
    return bool(chat)

# Check if a user is served
async def is_served_user(user_id: int) -> bool:
    user = await usersdb.find_one({"user_id": user_id})
    return bool(user)

# Utility to convert seconds into human-readable time
def get_readable_time(seconds: int) -> str:
    count = 0
    ping_time = ""
    time_list = []
    time_suffix_list = ["s", "m", "h", "days"]
    while count < 4:
        count += 1
        if count < 3:
            remainder, result = divmod(seconds, 60)
        else:
            remainder, result = divmod(seconds, 24)
        if seconds == 0 and remainder == 0:
            break
        time_list.append(int(result))
        seconds = int(remainder)
    for i in range(len(time_list)):
        time_list[i] = str(time_list[i]) + time_suffix_list[i]
    if len(time_list) == 4:
        ping_time += time_list.pop() + ", "
    time_list.reverse()
    ping_time += ":".join(time_list)
    return ping_time

# Stream Audio function with MongoDB checks and logging
@app.on_message(filters.command("play") & filters.group)
async def stream_audio(client, message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id

    # Check if the chat is served
    if not await is_served_chat(chat_id):
        await app.send_message(chat_id, "This chat is not authorized to use the bot.")
        return

    # Check if the user is served
    if not await is_served_user(user_id):
        await app.send_message(chat_id, "You are not authorized to use the bot.")
        return

    # Extract the query from the message
    query = message.text.split(' ', 1)[1] if len(message.text.split(' ', 1)) > 1 else None

    if query:
        # Log the song request to an external service (You can modify this method)
        log_message = f"Song requested: {query} by {message.from_user.mention}"
        await paste_queue(log_message)

        # Simulate searching for the audio URL (Replace with actual search and streaming logic)
        stream_url, title, duration = await search_and_get_audio_url(query)

        if stream_url:
            readable_duration = get_readable_time(duration)
            await app.send_message(chat_id, f"Now playing: {title}\nDuration: {readable_duration}")
            
            # Start streaming the audio
            audio_stream = AudioPiped(stream_url)
            await call.join_group_call(chat_id, audio_stream)
        else:
            await app.send_message(chat_id, "Couldn't find the song.")
    else:
        await app.send_message(chat_id, "Please provide a song to play.")

# Function to simulate getting the song URL (replace with actual search logic)
async def search_and_get_audio_url(query: str):
    # yt-dlp configuration for downloading or streaming audio from YouTube
    ydl_opts = {
        'format': 'bestaudio/best',
        'extractaudio': True,  # Download only audio
        'audioquality': 1,  # Best audio quality
        'outtmpl': 'downloads/%(id)s.%(ext)s',  # Download directory and filename format
        'quiet': True,  # Suppress output
        'cookies': 'cookies.txt',  # Path to your cookies.txt file for YouTube
    }

    with ytdl.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(f"ytsearch:{query}", download=False)
        if 'entries' in info_dict:
            video = info_dict['entries'][0]
            url = video['url']
            title = video['title']
            duration = video['duration']
            return url, title, duration
    return None, None, None

# Change stream function
async def change_stream(chat_id):
    queued = QUEUE.get(chat_id)
    if queued:
        queued.pop(0)
    if not queued:
        await app.send_message(chat_id, " ✼ Nᴏ ᴍᴏʀᴇ sᴏɴɢ, Sᴏ Lᴇғᴛ \nFʀᴏᴍ Vᴏɪᴄᴇ Cʜᴀᴛ❗...")
        return await close_stream(chat_id)

    title = queued[0].get("title")
    duration = queued[0].get("duration")
    stream_file = queued[0].get("stream_file")
    stream_type = queued[0].get("stream_type")
    try:
        requested_by = queued[0].get("user").mention
    except Exception:
        if queued[0].get("user").username:
            requested_by = (
                "["
                + queued[0].get("user").title
                + "](https://t.me/"
                + queued[0].get("user").username
                + ")"
            )
        else:
            requested_by = queued[0].get("user").title

    # Select media stream based on type
    if stream_type == "Audio":
        stream_media = MediaStream(
            media_path=stream_file,
            video_flags=MediaStream.Flags.IGNORE,
            audio_parameters=AudioQuality.STUDIO,
            ytdlp_parameters="--cookies cookies.txt",
        )
    elif stream_type == "Video":
        stream_media = MediaStream(
            media_path=stream_file,
            audio_parameters=AudioQuality.STUDIO,
            video_parameters=VideoQuality.HD_720p,
            ytdlp_parameters="--cookies cookies.txt",
        )

    await call.play(chat_id, stream_media)
    await add_active_media_chat(chat_id, stream_type)
    
    caption = f"""ꜱᴛᴀʀᴛᴇᴅ ꜱᴛʀᴇᴀᴍɪɴɢ ᴏɴ ᴠᴄ.
    
💫 Tɪᴛʟᴇ ❤️  {title}
🗡️ Dᴜʀᴀᴛɪᴏɴ ⏰  {duration}
🔉 Sᴛʀᴇᴀᴍ Tʏᴘᴇ 🔊  {stream_type}
💌 Rᴇǫᴜᴇsᴛᴇᴅ ʙʏ 💌  {requested_by}"""
    
    buttons = InlineKeyboardMarkup(
        [
            [
            InlineKeyboardButton(
                    text="🗑️ Stop Streaming",
                    callback_data=f"stop_{chat_id}"
                )
            ]
        ]
    )

    # Send a message with the stream info and control buttons
    await app.send_message(chat_id, caption, reply_markup=buttons)

# Stop stream function
async def close_stream(chat_id):
    # Leave the group call
    await call.leave_group_call(chat_id)

    # Remove chat from active lists
    await remove_active_media_chat(chat_id)

    # Notify users
    await app.send_message(chat_id, "Stream has been stopped.")

# Callback query handler to stop the stream
@app.on_callback_query(filters.regex(r"^stop_"))
async def stop_stream(client, callback_query):
    chat_id = int(callback_query.data.split("_")[1])

    # Check if the user who clicked the button is an admin
    if callback_query.from_user.id != chat_id:
        await callback_query.answer("You cannot stop the stream.", show_alert=True)
        return

    # Stop the stream
    await close_stream(chat_id)
    await callback_query.answer("Stream has been stopped.", show_alert=True)

# Utility to add songs to the queue
async def add_to_queue(chat_id, stream_file, stream_type, title, duration, user):
    if chat_id not in QUEUE:
        QUEUE[chat_id] = []

    QUEUE[chat_id].append({
        "stream_file": stream_file,
        "stream_type": stream_type,
        "title": title,
        "duration": duration,
        "user": user
    })

    # If no stream is active, start the first song in the queue
    if len(QUEUE[chat_id]) == 1:
        await change_stream(chat_id)

# Command to queue audio or video
@app.on_message(filters.command("queue") & filters.group)
async def queue_media(client, message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id

    # Check if the chat is served
    if not await is_served_chat(chat_id):
        await app.send_message(chat_id, "This chat is not authorized to use the bot.")
        return

    # Check if the user is served
    if not await is_served_user(user_id):
        await app.send_message(chat_id, "You are not authorized to use the bot.")
        return

    # Extract media details from the message (assuming the format of the message includes necessary data)
    stream_type = "Audio"  # Change based on the media type
    title = message.text.split(' ', 1)[1]  # Assuming the song name is the text following the command
    stream_file, title, duration = await search_and_get_audio_url(title)  # Search and get stream URL

    # Add to the queue and start streaming
    if stream_file:
        await add_to_queue(chat_id, stream_file, stream_type, title, duration, message.from_user)
    else:
        await app.send_message(chat_id, "Couldn't find the song.")
        
