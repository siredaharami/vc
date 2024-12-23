import asyncio
import random
from collections import deque
import requests
from pyrogram import *
from pyrogram import Client, filters
from pyrogram.errors.exceptions.flood_420 import FloodWait
from pyrogram.types import *
from pyrogram.types import Message

from BADUC.database.basic import edit_or_reply, get_text
from BADUC.database.constants import MEMES

from BADUC import SUDOERS
from BADUC.core.command import *

DEFAULTUSER = "Bad"

R = "❤️"
W = "🤍"

heart_list = [
    W * 9,
    W * 2 + R * 2 + W + R * 2 + W * 2,
    W + R * 7 + W,
    W + R * 7 + W,
    W + R * 7 + W,
    W * 2 + R * 5 + W * 2,
    W * 3 + R * 3 + W * 3,
    W * 4 + R + W * 4,
    W * 9,
]
joined_heart = "\n".join(heart_list)
heartlet_len = joined_heart.count(R)
SLEEP = 0.1


async def _wrap_edit(message, text: str):
    """Floodwait-safe utility wrapper for edit"""
    try:
        await message.edit(text)
    except FloodWait as fl:
        await asyncio.sleep(fl.x)


async def phase1(message):
    """Big scroll"""
    BIG_SCROLL = "🧡💛💚💙💜🖤🩷"
    await _wrap_edit(message, joined_heart)
    for heart in BIG_SCROLL:
        await _wrap_edit(message, joined_heart.replace(R, heart))
        await asyncio.sleep(SLEEP)


async def phase2(message):
    """Per-heart randomiser"""
    ALL = ["❤️"] + list("🧡💛💚💙💜🩷🖤")  # don't include white heart

    format_heart = joined_heart.replace(R, "{}")
    for _ in range(5):
        heart = format_heart.format(*random.choices(ALL, k=heartlet_len))
        await _wrap_edit(message, heart)
        await asyncio.sleep(SLEEP)


async def phase3(message):
    """Fill up heartlet matrix"""
    await _wrap_edit(message, joined_heart)
    await asyncio.sleep(SLEEP * 2)
    repl = joined_heart
    for _ in range(joined_heart.count(W)):
        repl = repl.replace(W, R, 1)
        await _wrap_edit(message, repl)
        await asyncio.sleep(SLEEP)


async def phase4(message):
    """Matrix shrinking"""
    for i in range(7, 0, -1):
        heart_matrix = "\n".join([R * i] * i)
        await _wrap_edit(message, heart_matrix)
        await asyncio.sleep(SLEEP)
        
@Client.on_message(bad(["sunset"]) & (filters.me | filters.user(SUDOERS)))
async def day_to_night(client: Client, message: Message):
    await phase1(message)
    await asyncio.sleep(SLEEP * 3)
    await message.edit("🌅")  # Sunrise
    await asyncio.sleep(1)
    await message.edit("🌞")  # Day
    await asyncio.sleep(1.5)
    await message.edit("🌤")  # Partly Cloudy
    await asyncio.sleep(1.5)
    await message.edit("🌇")  # Sunset
    await asyncio.sleep(1)
    await message.edit("🌙")  # Moonrise
    await asyncio.sleep(1.5)
    await message.edit("🌑")  # Night
    await asyncio.sleep(2)
    await message.edit("🌙🌑🌚🌒🌓🌔")  # Various moon phases

@Client.on_message(bad(["weather"]) & (filters.me | filters.user(SUDOERS)))
async def weather_animation(client: Client, message: Message):
    await phase1(message)
    await asyncio.sleep(SLEEP * 3)
    await message.edit("☀️")  # Sunny
    await asyncio.sleep(1)
    await message.edit("🌤")  # Partly Cloudy
    await asyncio.sleep(1.5)
    await message.edit("🌥")  # Overcast
    await asyncio.sleep(1)
    await message.edit("🌧")  # Rainy
    await asyncio.sleep(2)
    await message.edit("⛈")  # Thunderstorm
    await asyncio.sleep(2)
    await message.edit("🌨")  # Snowy
    await asyncio.sleep(1.5)
    await message.edit("🌬")  # Windy
    await asyncio.sleep(1.5)
    await message.edit("🌩")  # Thunderstorm (Again)
    await asyncio.sleep(3)
    await message.edit("🌤🌥🌧🌨🌬")  # Final mixed weather

@Client.on_message(bad(["nature"]) & (filters.me | filters.user(SUDOERS)))
async def nature_transition(client: Client, message: Message):
    await phase1(message)
    await asyncio.sleep(SLEEP * 3)
    await message.edit("🌄")  # Sunrise
    await asyncio.sleep(1.5)
    await message.edit("🌞")  # Daytime
    await asyncio.sleep(2)
    await message.edit("🌿")  # Nature/Plants growing
    await asyncio.sleep(2)
    await message.edit("🌳")  # Tree growth
    await asyncio.sleep(2)
    await message.edit("🌙")  # Nightfall
    await asyncio.sleep(1)
    await message.edit("🌑")  # Starry night
    await asyncio.sleep(1.5)
    await message.edit("🌠")  # Meteor Shower
    await asyncio.sleep(3)
    await message.edit("🌲🌳🌙🌑🌠")  # Final mixed nature scene

@Client.on_message(bad(["fire_ice"]) & (filters.me | filters.user(SUDOERS)))
async def fire_and_ice(client: Client, message: Message):
    await phase1(message)
    await asyncio.sleep(SLEEP * 3)
    await message.edit("🔥")  # Fire starts
    await asyncio.sleep(1)
    await message.edit("🌋")  # Volcano eruption
    await asyncio.sleep(2)
    await message.edit("❄️")  # Ice forms
    await asyncio.sleep(1)
    await message.edit("🌨")  # Snowstorm
    await asyncio.sleep(1.5)
    await message.edit("☃️")  # Snowman
    await asyncio.sleep(2)
    await message.edit("🔥❄️🌋🌨☃️")  # Fire and Ice combination

@Client.on_message(bad(["space"]) & (filters.me | filters.user(SUDOERS)))
async def space_journey(client: Client, message: Message):
    await phase1(message)
    await asyncio.sleep(SLEEP * 3)
    await message.edit("🌍")  # Earth
    await asyncio.sleep(1)
    await message.edit("🌑")  # The Moon
    await asyncio.sleep(1)
    await message.edit("🪐")  # Saturn (Planet)
    await asyncio.sleep(1.5)
    await message.edit("🚀")  # Rocket Launch
    await asyncio.sleep(2)
    await message.edit("🌠")  # Meteor Shower
    await asyncio.sleep(2)
    await message.edit("🌌")  # Galaxy
    await asyncio.sleep(3)
    await message.edit("🌍🌑🪐🚀🌠🌌")  # Final Space Journey

@Client.on_message(bad(["underwater"]) & (filters.me | filters.user(SUDOERS)))
async def underwater(client: Client, message: Message):
    await phase1(message)
    await asyncio.sleep(SLEEP * 3)
    await message.edit("🌊")  # Ocean
    await asyncio.sleep(1)
    await message.edit("🐠")  # Fish swimming
    await asyncio.sleep(1)
    await message.edit("🐙")  # Octopus
    await asyncio.sleep(2)
    await message.edit("🐋")  # Whale
    await asyncio.sleep(1)
    await message.edit("🐚")  # Shell
    await asyncio.sleep(1)
    await message.edit("🐬")  # Dolphin
    await asyncio.sleep(2)
    await message.edit("🌊🐠🐙🐋🐚🐬")  # Final underwater scene

@Client.on_message(bad(["fantasy"]) & (filters.me | filters.user(SUDOERS)))
async def fantasy_world(client: Client, message: Message):
    await phase1(message)
    await asyncio.sleep(SLEEP * 3)
    await message.edit("🧚")  # Fairy
    await asyncio.sleep(1)
    await message.edit("🦄")  # Unicorn
    await asyncio.sleep(1)
    await message.edit("🏰")  # Castle
    await asyncio.sleep(2)
    await message.edit("🌟")  # Magic sparkle
    await asyncio.sleep(1.5)
    await message.edit("🌈")  # Rainbow
    await asyncio.sleep(1)
    await message.edit("🧙‍♂️")  # Wizard
    await asyncio.sleep(2)
    await message.edit("🧚🦄🏰🌟🌈🧙‍♂️")  # Fantasy world complete

@Client.on_message(bad(["game"]) & (filters.me | filters.user(SUDOERS)))
async def game_animation(client: Client, message: Message):
    if message.forward_from:
        return
    animation_interval = 1
    animation_ttl = range(0, 14)
    await message.edit("🎮 Start Game")
    animation_chars = [
        "🎮 Loading... 1% \n\n🕹️",
        "🎮 Loading... 10% \n\n🕹️👾",
        "🎮 Loading... 25% \n\n👾🕹️💣",
        "🎮 Loading... 50% \n\n💣👾🕹️",
        "🎮 Loading... 75% \n\n💣💥🕹️👾",
        "🎮 Loading... 90% \n\n💥🔥👾🕹️",
        "🎮 Game Over 🕹️",
        "👾 Player 1: Level 1",
        "👾 Player 1: Level 2 🏆",
        "🕹️ Boss Fight!",
        "💥 Final Blow!",
        "🎉 You Win! 🏆",
        "🕹️ Next Level",
        "⚡ High Score: 999",
        "🎮 The End! Thanks for Playing!",
    ]
    for i in animation_ttl:
        await asyncio.sleep(animation_interval)
        await message.edit(animation_chars[i % 14])

@Client.on_message(bad(["space_exploration"]) & (filters.me | filters.user(SUDOERS)))
async def space_exploration(client: Client, message: Message):
    if message.forward_from:
        return
    animation_interval = 1
    animation_ttl = range(0, 14)
    await message.edit("🚀 Launching Space Mission")
    animation_chars = [
        "🚀 Launching in T-5 seconds...",
        "🚀 T-4... 🌕",
        "🚀 T-3... 🚀",
        "🚀 T-2... 🛰️",
        "🚀 T-1... 🛸",
        "🚀 Liftoff! 🌑",
        "🛸 Traveling through space... ✨",
        "👨‍🚀 Astronaut on mission... 🛸",
        "🌠 Passing through the stars... 🌌",
        "🚀 Entering the atmosphere... 🌍",
        "🌕 Approaching the Moon...",
        "🌑 Landing on the Moon... 🚀",
        "👨‍🚀 Astronaut walking on the moon... 🌕",
        "🌌 Mission Complete! 🚀",
        "🚀 The End - Thanks for joining the mission!",
    ]
    for i in animation_ttl:
        await asyncio.sleep(animation_interval)
        await message.edit(animation_chars[i % 14])

@Client.on_message(bad(["superhero"]) & (filters.me | filters.user(SUDOERS)))
async def superhero_fight(client: Client, message: Message):
    if message.forward_from:
        return
    animation_interval = 1
    animation_ttl = range(0, 14)
    await message.edit("🦸‍♂️ Superhero Fight!")
    animation_chars = [
        "🦸‍♂️ Hero vs Villain 🦹‍♂️",
        "💥 Fight Begins! ⚡",
        "🦸‍♂️ Hero Attacks! 💥",
        "🦹‍♂️ Villain Strikes Back! ⚡",
        "💥 Power Blast! 💨",
        "🦸‍♂️ Hero Wins! 🏆",
        "🦹‍♂️ Villain Escapes! 💨",
        "🦸‍♂️ Hero Rescues the City 🏙️",
        "💥 Epic Explosion! 💣",
        "🦸‍♂️ Victory! The City is Safe! 🏙️",
        "💪 Hero on Patrol 🚔",
        "🦸‍♂️ Hero Training for the Next Battle 🏋️‍♂️",
        "🏆 Superhero’s Day Off ☀️",
        "🦸‍♂️ The End of the Superhero Fight 🦹‍♂️",
    ]
    for i in animation_ttl:
        await asyncio.sleep(animation_interval)
        await message.edit(animation_chars[i % 14])


@Client.on_message(bad(["alarm"]) & (filters.me | filters.user(SUDOERS)))
async def alarm_animation(client: Client, message: Message):
    animation_interval = 0.3
    animation_ttl = range(0, 30)
    animation_chars = [
        "🟢🟢🟢🟢\n🟢🟢🟢🟢\n🟢🟢🟢🟢",
        "🟢🟢🟢🟢\n🟢🟡🟢🟢\n🟢🟢🟢🟢",
        "🟢🟡🟢🟢\n🟡🟢🟢🟢\n🟢🟢🟢🟢",
        "🟡🟢🟢🟢\n🟢🟡🟢🟢\n🟢🟢🟢🟢",
        "🟡🟡🟢🟢\n🟡🟡🟡🟡\n🟢🟢🟢🟢",
        "🟡🟢🟢🟡\n🟡🟢🟢🟡\n🟡🟢🟡🟡",
        "🟢🟡🟢🟢\n🟡🟢🟢🟡\n🟢🟡🟢🟢",
        "🟢🟢🟡🟡\n🟡🟡🟢🟡\n🟡🟢🟢🟢",
        "🟢🟢🟢🟡\n🟢🟡🟡🟢\n🟡🟢🟢🟢",
        "🚨🚨🚨🚨\n🚨🚨🚨🚨\n🚨🚨🚨🚨",
        "🔔🔔🔔🔔\n🔔🔔🔔🔔\n🔔🔔🔔🔔",
        "🚨🚨🚨🚨\n🚨🚨🚨🚨\n🚨🚨🚨🚨",
        "🔴🔴🔴🔴\n🔴🔴🔴🔴\n🔴🔴🔴🔴",
        "🟥🟥🟥🟥\n🟥🟥🟥🟥\n🟥🟥🟥🟥",
        "🚨 Alarm triggered! \nPlease evacuate immediately. \nStay calm and follow safety measures."
    ]
    if message.forward_from:
        return
    await message.edit("🔔 Alarm is ringing... 🚨")
    await asyncio.sleep(4)
    for i in animation_ttl:
        await asyncio.sleep(animation_interval)
        await message.edit(animation_chars[i % 14])

@Client.on_message(bad(["lights"]) & (filters.me | filters.user(SUDOERS)))
async def light_animation(client: Client, message: Message):
    animation_interval = 0.3
    animation_ttl = range(0, 30)
    animation_chars = [
        "💡💡💡💡\n💡💡💡💡\n💡💡💡💡",
        "💡💡💡💡\n💡💡💡💡\n💡💡💡💡",
        "💡💡💡💡\n💡💡💡💡\n💡💡💡💡",
        "💡💡💡💡\n💡💡💡💡\n💡💡💡💡",
        "🔆🔆🔆🔆\n🔆🔆🔆🔆\n🔆🔆🔆🔆",
        "🔆🔆🔆🔆\n🔆🔆🔆🔆\n🔆🔆🔆🔆",
        "🔅🔅🔅🔅\n🔅🔅🔅🔅\n🔅🔅🔅🔅",
        "💡💡💡💡\n💡💡💡💡\n💡💡💡💡",
        "🔅🔅🔅🔅\n🔅🔅🔅🔅\n🔅🔅🔅🔅",
        "💡💡💡💡\n💡💡💡💡\n💡💡💡💡",
        "🔆🔆🔆🔆\n🔆🔆🔆🔆\n🔆🔆🔆🔆",
        "💡💡💡💡\n💡💡💡💡\n💡💡💡💡",
        "🌟🌟🌟🌟\n🌟🌟🌟🌟\n🌟🌟🌟🌟",
        "🚨 Lights are flickering 🚨"
    ]
    if message.forward_from:
        return
    await message.edit("💡 Lights are flickering... 💡")
    await asyncio.sleep(4)
    for i in animation_ttl:
        await asyncio.sleep(animation_interval)
        await message.edit(animation_chars[i % 14])

@Client.on_message(bad(["warning"]) & (filters.me | filters.user(SUDOERS)))
async def warning_animation(client: Client, message: Message):
    animation_interval = 0.3
    animation_ttl = range(0, 30)
    animation_chars = [
        "⚠️⚠️⚠️⚠️\n⚠️⚠️⚠️⚠️\n⚠️⚠️⚠️⚠️",
        "⚠️⚠️⚠️⚠️\n⚠️⚠️⚠️⚠️\n⚠️⚠️⚠️⚠️",
        "⚠️⚠️⚠️⚠️\n⚠️⚠️⚠️⚠️\n⚠️⚠️⚠️⚠️",
        "⚠️⚠️⚠️⚠️\n⚠️⚠️⚠️⚠️\n⚠️⚠️⚠️⚠️",
        "🚨🚨🚨🚨\n🚨🚨🚨🚨\n🚨🚨🚨🚨",
        "🚨🚨🚨🚨\n🚨🚨🚨🚨\n🚨🚨🚨🚨",
        "⚠️⚠️⚠️⚠️\n⚠️⚠️⚠️⚠️\n⚠️⚠️⚠️⚠️",
        "⚠️⚠️⚠️⚠️\n⚠️⚠️⚠️⚠️\n⚠️⚠️⚠️⚠️",
        "🚨🚨🚨🚨\n🚨🚨🚨🚨\n🚨🚨🚨🚨",
        "⚠️⚠️⚠️⚠️\n⚠️⚠️⚠️⚠️\n⚠️⚠️⚠️⚠️",
        "⚠️⚠️⚠️⚠️\n⚠️⚠️⚠️⚠️\n⚠️⚠️⚠️⚠️",
        "🚨🚨🚨🚨\n🚨🚨🚨🚨\n🚨🚨🚨🚨",
        "⚠️⚠️⚠️⚠️\n⚠️⚠️⚠️⚠️\n⚠️⚠️⚠️⚠️",
        "🚨 Warning: System Overload 🚨"
    ]
    if message.forward_from:
        return
    await message.edit("⚠️ Warning... ⚠️")
    await asyncio.sleep(4)
    for i in animation_ttl:
        await asyncio.sleep(animation_interval)
        await message.edit(animation_chars[i % 14])

@Client.on_message(bad(["bad2"]) & (filters.me | filters.user(SUDOERS)))
async def okihakga(client: Client, message: Message):
    if message.forward_from:
        return
    animation_interval = 0.3
    animation_ttl = range(0, 15)
    await message.edit("bad....")
    animation_chars = [
        "⬜⬜⬜⬜⬜⬜⬜\n⬜⬜⬜⬜⬜⬜⬜\n⬜⬜⬜⬜⬜⬜⬜\n⬜⬜⬜⬜⬜⬜⬜\n⬜⬜⬜⬜⬜⬜⬜\n⬜⬜⬜⬜⬜⬜⬜\n⬜⬜⬜⬜⬜⬜⬜",
        "⬜⬜⬜⬜⬜⬜⬜\n⬜⬜⬜⬜⬜⬜⬜\n⬜⬜⬜⬜⬜⬜⬜\n⬜⬜⬜⬛⬜⬜⬜\n⬜⬜⬜⬜⬜⬜⬜\n⬜⬜⬜⬜⬜⬜⬜\n⬜⬜⬜⬜⬜⬜⬜",
        "⬜⬜⬜⬜⬜⬜⬜\n⬜⬜⬜⬜⬜⬜⬜\n⬜⬜⬛⬛⬛⬜⬜\n⬜⬜⬛⬜⬛⬜⬜\n⬜⬜⬛⬛⬛⬜⬜\n⬜⬜⬜⬜⬜⬜⬜\n⬜⬜⬜⬜⬜⬜⬜",
        "⬜⬜⬜⬜⬜⬜⬜\n⬜⬛⬛⬛⬛⬛⬜\n⬜⬛⬜⬜⬜⬛⬜\n⬜⬛⬜⬜⬜⬛⬜\n⬜⬛⬜⬜⬜⬛⬜\n⬜⬛⬛⬛⬛⬛⬜\n⬜⬜⬜⬜⬜⬜⬜",
        "⬛⬛⬛⬛⬛⬛⬛\n⬛⬜⬜⬜⬜⬜⬛\n⬛⬜⬜⬜⬜⬜⬛\n⬛⬜⬜⬜⬜⬜⬛\n⬛⬜⬜⬜⬜⬜⬛\n⬛⬜⬜⬜⬜⬜⬛\n⬛⬛⬛⬛⬛⬛⬛",
        "⬛⬜⬛⬜⬛⬜⬛⬜\n⬜⬛⬜⬛⬜⬛⬜⬛\n⬛⬜⬛⬜⬛⬜⬛⬜\n⬜⬛⬜⬛⬜⬛⬜⬛\n⬛⬜⬛⬜⬛⬛⬛⬜\n⬜⬛⬛⬛⬛⬛⬛⬜\n⬛⬜⬛⬛⬛⬛⬛⬛",
        "⬜⬛⬜⬛⬜⬛⬜⬛\n⬛⬜⬛⬜⬛⬜⬛⬜\n⬜⬛⬜⬛⬜⬛⬛⬛\n⬛⬜⬛⬜⬛⬛⬛⬛\n⬜⬛⬛⬛⬛⬛⬛⬛\n⬛⬛⬛⬛⬛⬛⬛⬛\n⬛⬜⬛⬛⬛⬛⬛⬛",
        "⬜⬜⬜⬜⬜⬜⬜\n⬜⬛⬛⬛⬛⬛⬜\n⬜⬛⬜⬜⬜⬛⬜\n⬜⬛⬜⬛⬛⬛⬛\n⬜⬛⬛⬛⬛⬛⬛\n⬜⬛⬛⬛⬛⬛⬛\n⬜⬜⬜⬜⬜⬜⬜",
        "⬛⬛⬛⬛⬛⬛⬛\n⬛⬜⬜⬜⬜⬜⬛\n⬛⬜⬛⬛⬛⬜⬛\n⬛⬜⬛⬛⬛⬛⬛\n⬛⬛⬛⬛⬛⬛⬛\n⬛⬛⬛⬛⬛⬛⬛\n⬛⬛⬛⬛⬛⬛⬛",
        "⬜⬜⬜⬜⬜⬜⬜\n⬜⬛⬛⬛⬛⬛⬜\n⬜⬛⬜⬜⬜⬛⬜\n⬜⬛⬛⬛⬛⬛⬛\n⬜⬛⬛⬛⬛⬛⬛\n⬜⬛⬛⬛⬛⬛⬛\n⬜⬜⬜⬜⬜⬜⬜",
        "⬛⬛⬛⬛⬛⬛⬛\n⬛⬜⬜⬜⬜⬜⬛\n⬛⬜⬛⬛⬛⬛⬛\n⬛⬛⬛⬛⬛⬛⬛\n⬛⬛⬛⬛⬛⬛⬛\n⬛⬛⬛⬛⬛⬛⬛\n⬛⬛⬛⬛⬛⬛⬛",
        "⬜⬜⬜⬜⬜⬜⬜\n⬜⬛⬛⬛⬛⬛⬜\n⬜⬛⬜⬜⬜⬛⬜\n⬜⬛⬛⬛⬛⬛⬛\n⬜⬛⬛⬛⬛⬛⬛\n⬜⬛⬛⬛⬛⬛⬛\n⬜⬜⬜⬜⬜⬜⬜",
        "⬛⬛⬛⬛⬛⬛⬛\n⬛⬜⬜⬜⬜⬜⬛\n⬛⬛⬛⬛⬛⬛⬛\n⬛⬛⬛⬛⬛⬛⬛\n⬛⬛⬛⬛⬛⬛⬛\n⬛⬛⬛⬛⬛⬛⬛\n⬛⬛⬛⬛⬛⬛⬛",
        "⬜⬜⬜⬜⬜⬜⬜\n⬜⬛⬛⬛⬛⬛⬜\n⬜⬛⬛⬛⬛⬛⬛\n⬜⬛⬛⬛⬛⬛⬛\n⬜⬛⬛⬛⬛⬛⬛\n⬜⬛⬛⬛⬛⬛⬛\n⬜⬜⬜⬜⬜⬜⬜",
    ]
    for i in animation_ttl:
        await asyncio.sleep(animation_interval)
        await message.edit(animation_chars[i % 15])

@Client.on_message(bad(["shizu"]) & (filters.me | filters.user(SUDOERS)))
async def okihakga(client: Client, message: Message):
    if message.forward_from:
        return
    animation_interval = 0.3
    animation_ttl = range(0, 15)
    await message.edit("shizu....")
    animation_chars = [
        "❤️💜❤️💜❤️💜❤️\n❤️💜❤️💜❤️💜❤️\n❤️💜❤️💜❤️💜❤️\n❤️💜❤️💜❤️💜❤️\n❤️💜❤️💜❤️💜❤️\n❤️💜❤️💜❤️💜❤️\n❤️💜❤️💜❤️💜❤️",
        "💜❤️💜❤️💜❤️💜\n💜❤️💜❤️💜❤️💜\n💜❤️💜❤️💜❤️💜\n💜❤️💜❤️💜❤️💜\n💜❤️💜❤️💜❤️💜\n💜❤️💜❤️💜❤️💜\n💜❤️💜❤️💜❤️💜",
        "❤️💜❤️💜❤️💜❤️\n❤️💜❤️💜❤️💜❤️\n❤️💜❤️💜❤️💜❤️\n❤️💜❤️💜❤️💜❤️\n❤️💜❤️💜❤️💜❤️\n❤️💜❤️💜❤️💜❤️\n❤️💜❤️💜❤️💜❤️",
        "💜❤️💜❤️💜❤️💜\n💜❤️💜❤️💜❤️💜\n💜❤️💜❤️💜❤️💜\n💜❤️💜❤️💜❤️💜\n💜❤️💜❤️💜❤️💜\n💜❤️💜❤️💜❤️💜\n💜❤️💜❤️💜❤️💜",
        "❤️💜❤️💜❤️💜❤️\n❤️💜❤️💜❤️💜❤️\n❤️💜❤️💜❤️💜❤️\n❤️💜❤️💜❤️💜❤️\n❤️💜❤️💜❤️💜❤️\n❤️💜❤️💜❤️💜❤️\n❤️💜❤️💜❤️💜❤️",
        "💜❤️💜❤️💜❤️💜\n💜❤️💜❤️💜❤️💜\n💜❤️💜❤️💜❤️💜\n💜❤️💜❤️💜❤️💜\n💜❤️💜❤️💜❤️💜\n💜❤️💜❤️💜❤️💜\n💜❤️💜❤️💜❤️💜",
        "❤️💜❤️💜❤️💜❤️\n❤️💜❤️💜❤️💜❤️\n❤️💜❤️💜❤️💜❤️\n❤️💜❤️💜❤️💜❤️\n❤️💜❤️💜❤️💜❤️\n❤️💜❤️💜❤️💜❤️\n❤️💜❤️💜❤️💜❤️",
        "💜❤️💜❤️💜❤️💜\n💜❤️💜❤️💜❤️💜\n💜❤️💜❤️💜❤️💜\n💜❤️💜❤️💜❤️💜\n💜❤️💜❤️💜❤️💜\n💜❤️💜❤️💜❤️💜\n💜❤️💜❤️💜❤️💜",
        "❤️💜❤️💜❤️💜❤️\n❤️💜❤️💜❤️💜❤️\n❤️💜❤️💜❤️💜❤️\n❤️💜❤️💜❤️💜❤️\n❤️💜❤️💜❤️💜❤️\n❤️💜❤️💜❤️💜❤️\n❤️💜❤️💜❤️💜❤️",
        "💜❤️💜❤️💜❤️💜\n💜❤️💜❤️💜❤️💜\n💜❤️💜❤️💜❤️💜\n💜❤️💜❤️💜❤️💜\n💜❤️💜❤️💜❤️💜\n💜❤️💜❤️💜❤️💜\n💜❤️💜❤️💜❤️💜",
        "❤️💜❤️💜❤️💜❤️\n❤️💜❤️💜❤️💜❤️\n❤️💜❤️💜❤️💜❤️\n❤️💜❤️💜❤️💜❤️\n❤️💜❤️💜❤️💜❤️\n❤️💜❤️💜❤️💜❤️\n❤️💜❤️💜❤️💜❤️",
        "💜❤️💜❤️💜❤️💜\n💜❤️💜❤️💜❤️💜\n💜❤️💜❤️💜❤️💜\n💜❤️💜❤️💜❤️💜\n💜❤️💜❤️💜❤️💜\n💜❤️💜❤️💜❤️💜\n💜❤️💜❤️💜❤️💜",
        "❤️💜❤️💜❤️💜❤️\n❤️💜❤️💜❤️💜❤️\n❤️💜❤️💜❤️💜❤️\n❤️💜❤️💜❤️💜❤️\n❤️💜❤️💜❤️💜❤️\n❤️💜❤️💜❤️💜❤️\n❤️💜❤️💜❤️💜❤️",
        "💜❤️💜❤️💜❤️💜\n💜❤️💜❤️💜❤️💜\n💜❤️💜❤️💜❤️💜\n💜❤️💜❤️💜❤️💜\n💜❤️💜❤️💜❤️💜\n💜❤️💜❤️💜❤️💜\n💜❤️💜❤️💜❤️💜",
    ]
    for i in animation_ttl:
        await asyncio.sleep(animation_interval)
        await message.edit(animation_chars[i % 15])


@Client.on_message(bad(["hours"]) & (filters.me | filters.user(SUDOERS)))
async def ngefuck(client: Client, message: Message):
    e = await edit_or_reply(message, ".                       /¯ )")
    await e.edit(".                       /¯ )\n                      /¯  /")
    await e.edit(
        ".                       /¯ )\n                      /¯  /\n                    /    /"
    )
    await e.edit(
        ".                       /¯ )\n                      /¯  /\n                    /    /\n              /´¯/'   '/´¯¯`•¸"
    )
    await e.edit(
        ".                       /¯ )\n                      /¯  /\n                    /    /\n              /´¯/'   '/´¯¯`•¸\n          /'/   /    /       /¨¯\\ "
    )
    await e.edit(
        ".                       /¯ )\n                      /¯  /\n                    /    /\n              /´¯/'   '/´¯¯`•¸\n          /'/   /    /       /¨¯\\ \n        ('(   (   (   (  ¯~/'  ')"
    )
    await e.edit(
        ".                       /¯ )\n                      /¯  /\n                    /    /\n              /´¯/'   '/´¯¯`•¸\n          /'/   /    /       /¨¯\\ \n        ('(   (   (   (  ¯~/'  ')\n         \\                        /"
    )
    await e.edit(
        ".                       /¯ )\n                      /¯  /\n                    /    /\n              /´¯/'   '/´¯¯`•¸\n          /'/   /    /       /¨¯\\ \n        ('(   (   (   (  ¯~/'  ')\n         \\                        /\n          \\                _.•´"
    )
    await e.edit(
        ".                       /¯ )\n                      /¯  /\n                    /    /\n              /´¯/'   '/´¯¯`•¸\n          /'/   /    /       /¨¯\\ \n        ('(   (   (   (  ¯~/'  ')\n         \\                        /\n          \\                _.•´\n            \\              ("
    )
    await e.edit(
        ".                       /¯ )\n                      /¯  /\n                    /    /\n              /´¯/'   '/´¯¯`•¸\n          /'/   /    /       /¨¯\\ \n        ('(   (   (   (  ¯~/'  ')\n         \\                        /\n          \\                _.•´\n            \\              (\n              \\  "
    )
    await e.edit(
        ".                       /¯ )\n                      /¯  /\n                    /    /\n              /´¯/'   '/´¯¯`•¸\n          /'/   /    /       /¨¯\\ \n        ('(   (   (   (  ¯~/'  ')\n         \\                        /\n          \\                _.•´\n            \\              (\n              \\  H"
    )
    await asyncio.sleep(0.5)  # Slow motion effect for transition
    await e.edit(
        ".                       /¯ )\n                      /¯  /\n                    /    /\n              /´¯/'   '/´¯¯`•¸\n          /'/   /    /       /¨¯\\ \n        ('(   (   (   (  ¯~/'  ')\n         \\                        /\n          \\                _.•´\n            \\              (\n              \\  H  O"
    )
    await asyncio.sleep(0.5)
    await e.edit(
        ".                       /¯ )\n                      /¯  /\n                    /    /\n              /´¯/'   '/´¯¯`•¸\n          /'/   /    /       /¨¯\\ \n        ('(   (   (   (  ¯~/'  ')\n         \\                        /\n          \\                _.•´\n            \\              (\n              \\  H  O  U"
    )
    await asyncio.sleep(0.5)
    await e.edit(
        ".                       /¯ )\n                      /¯  /\n                    /    /\n              /´¯/'   '/´¯¯`•¸\n          /'/   /    /       /¨¯\\ \n        ('(   (   (   (  ¯~/'  ')\n         \\                        /\n          \\                _.•´\n            \\              (\n              \\  H  O  U  R"
    )
    await asyncio.sleep(0.5)
    await e.edit(
        ".                       /¯ )\n                      /¯  /\n                    /    /\n              /´¯/'   '/´¯¯`•¸\n          /'/   /    /       /¨¯\\ \n        ('(   (   (   (  ¯~/'  ')\n         \\                        /\n          \\                _.•´\n            \\              (\n              \\  H  O  U  R  S"
    )


__NAME__ = "ᴀɴɪᴍᴀᴛɪᴏɴ ₃"
__MENU__ = """
`.sunset` ᴛʏᴘᴇ sᴜɴsᴇᴛ ᴀɴᴅ sᴇᴇ ᴍᴀɢɪᴄ.

`.weather` ᴛʏᴘᴇ ᴡᴇᴀᴛʜᴇʀ ᴀɴᴅ sᴇᴇ ᴍᴀɢɪᴄ.

`.nature` ᴛʏᴘᴇ ɴᴀᴛᴜʀᴇ ᴀɴᴅ sᴇᴇ ᴍᴀɢɪᴄ.

`.fire_ice` ᴛʏᴘᴇ ғɪʀᴇ_ɪᴄᴇ ᴀɴᴅ sᴇᴇ ᴍᴀɢɪᴄ.

`.space` ᴛʏᴘᴇ sᴘᴀᴄᴇ ᴀɴᴅ sᴇᴇ ᴍᴀɢɪᴄ.

`.underwater` ᴛʏᴘᴇ ᴜɴᴅᴇʀᴡᴀᴛᴇʀ ᴀɴᴅ sᴇᴇ ᴍᴀɢɪᴄ.

`.fantasy` ᴛʏᴘᴇ ғᴀɴᴛᴀsʏ ᴀɴᴅ sᴇᴇ ᴍᴀɢɪᴄ.

`.game` ᴛʏᴘᴇ ɢᴀᴍᴇ ᴀɴᴅ sᴇᴇ ᴍᴀɢɪᴄ.

`.space_exploration` ᴛʏᴘᴇ sᴘᴀᴄᴇ_ᴇxᴘʟᴏʀᴀᴛɪᴏɴ ᴀɴᴅ sᴇᴇ ᴍᴀɢɪᴄ.

`.superhero` ᴛʏᴘᴇ sᴜᴘᴇʀʜᴇʀᴏ ᴀɴᴅ sᴇᴇ ᴍᴀɢɪᴄ.

`.alarm` ᴛʏᴘᴇ ᴀʟᴀʀᴍ ᴀɴᴅ sᴇᴇ ᴍᴀɢɪᴄ.

`.lights` ᴛʏᴘᴇ ʟɪɢʜᴛs ᴀɴᴅ sᴇᴇ ᴍᴀɢɪᴄ.

`.warning` ᴛʏᴘᴇ ᴡᴀʀɴɪɴɢ ᴀɴᴅ sᴇᴇ ᴍᴀɢɪᴄ.

`.badd` ᴛʏᴘᴇ ʙᴀᴅᴅ ᴀɴᴅ sᴇᴇ ᴍᴀɢɪᴄ.

`.shizu` ᴛʏᴘᴇ sʜɪᴢᴜ ᴀɴᴅ sᴇᴇ ᴍᴀɢɪᴄ.

`.hours` ᴛʏᴘᴇ ʜᴏᴜʀs ᴀɴᴅ sᴇᴇ ᴍᴀɢɪᴄ.
"""
