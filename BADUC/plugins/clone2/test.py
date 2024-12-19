from pyrogram import Client, filters

@Client.on_message(filters.command("test"))
async def test_command(client, message):
    await message.reply("The plugin is working correctly!")
