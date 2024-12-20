from pyrogram import Client, filters
import random

games = {}

# Command to start the Ludo game
@bot.on_message(filters.command("start_ludo"))
async def start_ludo(client, message):
    player_id = message.from_user.id
    
    # Check if a game already exists for the player
    if player_id in games:
        await message.reply("You are already in a game!")
    else:
        # Start a new game
        games[player_id] = {
            "players": [player_id],
            "board": [0] * 4,  # For simplicity, a 4-cell board for each player
            "turn": 0,
            "status": "waiting"  # waiting, playing, finished
        }
        await message.reply("Welcome to Ludo! You are the first player. Waiting for another player to join...")

# Command to join the game
@bot.on_message(filters.command("join_ludo"))
async def join_ludo(client, message):
    player_id = message.from_user.id
    
    # Check if the game exists and is in waiting status
    for game in games.values():
        if game["status"] == "waiting" and player_id not in game["players"]:
            game["players"].append(player_id)
            game["status"] = "playing"
            await message.reply("You have joined the game!")
            await start_turn(client, game)
            return
    
    await message.reply("No game available to join or game already in progress.")

# Function to start a player's turn
async def start_turn(client, game):
    player = game["players"][game["turn"]]
    await client.send_message(player, "Your turn! Roll the dice using /roll_ludo")

# Command to roll the dice
@bot.on_message(filters.command("roll_ludo"))
async def roll_ludo(client, message):
    player_id = message.from_user.id
    
    # Check if the player is in a game
    for game in games.values():
        if player_id in game["players"] and game["status"] == "playing":
            if player_id != game["players"][game["turn"]]:
                await message.reply("It's not your turn yet!")
                return
            
            # Roll the dice
            dice_roll = random.randint(1, 6)
            await message.reply(f"You rolled a {dice_roll}")
            
            # Update the board (simple logic for now)
            player_index = game["players"].index(player_id)
            game["board"][player_index] += dice_roll
            if game["board"][player_index] >= 4:  # End game condition (simplified)
                game["status"] = "finished"
                await message.reply(f"Player {message.from_user.first_name} wins!")
                return

            # Change turn
            game["turn"] = (game["turn"] + 1) % len(game["players"])
            await start_turn(client, game)
            return
    
    await message.reply("You are not in a game yet!")
