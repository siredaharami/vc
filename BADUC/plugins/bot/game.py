from pyrogram import Client, filters
import random
from BADUC.core.clients import bot
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

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

def update_board(game_id, user_id, position):
    board = game_state[game_id]['board']
    if board[position] == ' ':
        board[position] = 'X' if game_state[game_id]['turn'] == 'X' else 'O'
        winner = check_winner(board)
        game_state[game_id]['turn'] = 'O' if game_state[game_id]['turn'] == 'X' else 'X'
        return (board, winner)
    return (board, None)

def get_board_message(board):
    board_str = "\n".join([" | ".join(board[i:i+3]) for i in range(0, 9, 3)])
    return f"Current Board:\n{board_str}"

# Start Game
@bot.on_message(filters.command("games"))
async def start_game(client, message):
    buttons = [
        [InlineKeyboardButton("Tic-Tac-Toe", callback_data="tic_tac_toe"),
         InlineKeyboardButton("Number Guessing", callback_data="guess_game"),
         InlineKeyboardButton("Rock, Paper, Scissors", callback_data="rps_game")]
    ]
    keyboard = InlineKeyboardMarkup(buttons)
    await message.reply("Choose a game to play:", reply_markup=keyboard)

# Tic-Tac-Toe Game
@bot.on_callback_query(filters.regex("tic_tac_toe"))
async def start_tic_tac_toe(client, callback_query):
    user_id = callback_query.from_user.id
    game_id = f"game_{user_id}"  # Unique game ID per user
    game_state[game_id] = {'board': create_board(), 'turn': 'X', 'players': [user_id, None]}
    
    buttons = [
        [InlineKeyboardButton("Start game with a friend", callback_data="join_game")]
    ]
    keyboard = InlineKeyboardMarkup(buttons)
    await callback_query.message.edit_text("Game started! Waiting for another player to join...", reply_markup=keyboard)

@bot.on_callback_query(filters.regex("join_game"))
async def join_game(client, callback_query):
    user_id = callback_query.from_user.id
    game_id = f"game_{callback_query.message.chat.id}"  # Using chat.id to identify the game
    if game_id not in game_state:
        return
    
    game_state[game_id]['players'][1] = user_id
    buttons = [
        [InlineKeyboardButton(str(i), callback_data=f"play_{i}_{game_id}") for i in range(3)],
        [InlineKeyboardButton(str(i + 3), callback_data=f"play_{i + 3}_{game_id}") for i in range(3)],
        [InlineKeyboardButton(str(i + 6), callback_data=f"play_{i + 6}_{game_id}") for i in range(3)]
    ]
    keyboard = InlineKeyboardMarkup(buttons)
    await callback_query.message.edit_text(f"Game started! Your turn (X), Player 1: {game_state[game_id]['players'][0]}, Player 2: {user_id}.", reply_markup=keyboard)

@bot.on_callback_query(filters.regex("play_"))
async def play_tic_tac_toe(client, callback_query):
    user_id = callback_query.from_user.id
    position = int(callback_query.data.split("_")[1])
    game_id = callback_query.data.split("_")[2]

    # Ensure only the current player's turn
    if game_state[game_id]['players'][game_state[game_id]['turn'] == 'X'] != user_id:
        await callback_query.answer("It's not your turn!", show_alert=True)
        return

    board, winner = update_board(game_id, user_id, position)
    
    # Check for a winner
    if winner:
        await callback_query.edit_message_text(f"{winner} wins!\n{get_board_message(board)}")
        del game_state[game_id]
    else:
        # Update the game state and show the next player's turn
        next_turn = game_state[game_id]['turn']
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton(str(i), callback_data=f"play_{i}_{game_id}") for i in range(3)],
            [InlineKeyboardButton(str(i + 3), callback_data=f"play_{i + 3}_{game_id}") for i in range(3)],
            [InlineKeyboardButton(str(i + 6), callback_data=f"play_{i + 6}_{game_id}") for i in range(3)]
        ])
        await callback_query.edit_message_text(f"Next turn: {next_turn}\n{get_board_message(board)}", reply_markup=keyboard)

# Number Guessing Game
def start_guess_game(user_id):
    game_state[user_id] = random.randint(1, 100)

@bot.on_callback_query(filters.regex("guess_game"))
async def start_number_game(client, callback_query):
    user_id = callback_query.from_user.id
    start_guess_game(user_id)
    await callback_query.message.edit_text("I have selected a number between 1 and 100. Guess the number!")

@bot.on_message(filters.text)
async def guess_number(client, message):
    user_id = message.from_user.id
    if user_id in game_state and isinstance(game_state[user_id], int):
        try:
            guess = int(message.text)
            result = check_guess(user_id, guess)
            await message.reply(result)
        except ValueError:
            await message.reply("Please enter a valid number.")

# Rock, Paper, Scissors
@bot.on_callback_query(filters.regex("rps_game"))
async def start_rps_game(client, callback_query):
    buttons = [
        [InlineKeyboardButton("Rock", callback_data="rps_rock"),
         InlineKeyboardButton("Paper", callback_data="rps_paper"),
         InlineKeyboardButton("Scissors", callback_data="rps_scissors")]
    ]
    keyboard = InlineKeyboardMarkup(buttons)
    await callback_query.message.edit_text("Choose Rock, Paper, or Scissors:", reply_markup=keyboard)

@bot.on_callback_query(filters.regex("rps_"))
async def play_rps(client, callback_query):
    user_choice = callback_query.data.split("_")[1]
    result = play_rps_logic(user_choice)  # Calling the function to get the result
    await callback_query.edit_message_text(result)

def play_rps_logic(user_choice):
    choices = ["rock", "paper", "scissors"]
    bot_choice = random.choice(choices)
    if user_choice == bot_choice:
        return f"Both chose {user_choice}. It's a tie!"
    if (user_choice == "rock" and bot_choice == "scissors") or \
       (user_choice == "paper" and bot_choice == "rock") or \
       (user_choice == "scissors" and bot_choice == "paper"):
        return f"You win! I chose {bot_choice}."
    return f"You lose! I chose {bot_choice}."
