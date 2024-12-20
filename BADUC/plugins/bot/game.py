from pyrogram import Client, filters
import random
from BADUC.core.clients import bot
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, InputTextMessageContent


# Game states
game_state = {}

# Tic-Tac-Toe Game
def create_board():
    return [' ' for _ in range(9)]

def check_winner(board):
    winning_combinations = [(0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6)]
    for a, b, c in winning_combinations:
        if board[a] == board[b] == board[c] and board[a] != ' ':
            return board[a]
    return None

def update_board(user_id, position):
    board = game_state[user_id]['board']
    if board[position] == ' ':
        board[position] = 'X' if game_state[user_id]['turn'] == 'X' else 'O'
        winner = check_winner(board)
        game_state[user_id]['turn'] = 'O' if game_state[user_id]['turn'] == 'X' else 'X'
        return (board, winner)
    return (board, None)

def get_board_message(board):
    board_str = "\n".join([" | ".join(board[i:i+3]) for i in range(0, 9, 3)])
    return f"Current Board:\n{board_str}"

# Number Guessing Game
def start_guess_game(user_id):
    game_state[user_id] = random.randint(1, 100)

def check_guess(user_id, guess):
    if user_id not in game_state:
        return None
    target = game_state[user_id]
    if guess < target:
        return "Too low!"
    elif guess > target:
        return "Too high!"
    else:
        del game_state[user_id]
        return f"Correct! The number was {target}. You win!"

# Rock Paper Scissors
def play_rps(user_choice):
    choices = ["rock", "paper", "scissors"]
    bot_choice = random.choice(choices)
    if user_choice == bot_choice:
        return f"Both chose {user_choice}. It's a tie!"
    if (user_choice == "rock" and bot_choice == "scissors") or \
       (user_choice == "paper" and bot_choice == "rock") or \
       (user_choice == "scissors" and bot_choice == "paper"):
        return f"You win! I chose {bot_choice}."
    return f"You lose! I chose {bot_choice}."

# Tic-Tac-Toe Command
@bot.on_message(filters.command("tic_tac_toe"))
async def start_tic_tac_toe(client, message):
    user_id = message.from_user.id
    game_state[user_id] = {'board': create_board(), 'turn': 'X', 'players': [message.from_user.id, None]}
    await message.reply("Game started! Your turn (X).")

@bot.on_message(filters.command("play"))
async def play_tic_tac_toe(client, message):
    user_id = message.from_user.id
    if user_id not in game_state:
        await message.reply("Start a Tic-Tac-Toe game first by using /tic_tac_toe.")
        return
    if len(message.command) < 2:
        await message.reply("Please provide a position (0-8) to play.")
        return
    try:
        position = int(message.command[1])
        if position < 0 or position > 8:
            await message.reply("Invalid position. Please choose a number between 0 and 8.")
            return
    except ValueError:
        await message.reply("Please provide a valid number for the position.")
        return
    
    board, winner = update_board(user_id, position)
    
    if winner:
        await message.reply(f"{winner} wins!\n{get_board_message(board)}")
        del game_state[user_id]
    else:
        next_turn = game_state[user_id]['turn']
        await message.reply(f"Next turn: {next_turn}\n{get_board_message(board)}")

# Number Guessing Game Command
@bot.on_message(filters.command("guess_game"))
async def start_number_game(client, message):
    user_id = message.from_user.id
    start_guess_game(user_id)
    await message.reply("I have selected a number between 1 and 100. Guess the number!")

@bot.on_message(filters.command("guess"))
async def guess_number(client, message):
    user_id = message.from_user.id
    if user_id in game_state and isinstance(game_state[user_id], int):
        try:
            guess = int(message.text.split(" ")[1])
            result = check_guess(user_id, guess)
            await message.reply(result)
        except ValueError:
            await message.reply("Please enter a valid number after the command.")
    else:
        await message.reply("No guessing game has been started. Use /guess_game to start one.")

# Rock, Paper, Scissors Command
@bot.on_message(filters.command("rps"))
async def start_rps_game(client, message):
    if len(message.command) < 2:
        await message.reply("Please choose rock, paper, or scissors.")
        return
    user_choice = message.command[1].lower()
    if user_choice not in ["rock", "paper", "scissors"]:
        await message.reply("Invalid choice. Choose between rock, paper, or scissors.")
        return
    
    result = play_rps(user_choice)
    await message.reply(result)
