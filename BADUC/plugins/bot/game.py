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
    winning_combinations = [
        (0, 1, 2), (3, 4, 5), (6, 7, 8),
        (0, 3, 6), (1, 4, 7), (2, 5, 8),
        (0, 4, 8), (2, 4, 6)
    ]
    for a, b, c in winning_combinations:
        if board[a] == board[b] == board[c] and board[a] != ' ':
            return board[a]
    return None

def update_board(chat_id, position):
    board = game_state[chat_id]['board']
    if board[position] == ' ':
        current_turn = game_state[chat_id]['turn']
        board[position] = current_turn
        winner = check_winner(board)
        game_state[chat_id]['turn'] = 'O' if current_turn == 'X' else 'X'
        return board, winner
    return board, None

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
    chat_id = callback_query.message.chat.id
    game_state[chat_id] = {
        'board': create_board(),
        'turn': 'X',
        'players': [callback_query.from_user.id, None]
    }
    buttons = [[InlineKeyboardButton("Start Game with a Friend", callback_data=f"join_game_{chat_id}")]]
    keyboard = InlineKeyboardMarkup(buttons)
    await callback_query.message.edit_text("Tic-Tac-Toe started! Waiting for a friend to join.", reply_markup=keyboard)

@bot.on_callback_query(filters.regex(r"join_game_"))
async def join_game(client, callback_query):
    chat_id = int(callback_query.data.split("_")[2])
    user_id = callback_query.from_user.id

    if game_state[chat_id]['players'][1] is None:
        game_state[chat_id]['players'][1] = user_id
        await callback_query.message.edit_text("Friend joined! Let's start the game.")

        # Display the board
        buttons = [
            [InlineKeyboardButton(str(i), callback_data=f"play_{i}_{chat_id}") for i in range(3)],
            [InlineKeyboardButton(str(i + 3), callback_data=f"play_{i + 3}_{chat_id}") for i in range(3)],
            [InlineKeyboardButton(str(i + 6), callback_data=f"play_{i + 6}_{chat_id}") for i in range(3)]
        ]
        keyboard = InlineKeyboardMarkup(buttons)
        await callback_query.message.reply("Game started! Your turn (X).", reply_markup=keyboard)
    else:
        await callback_query.answer("A friend has already joined the game!", show_alert=True)

@bot.on_callback_query(filters.regex(r"play_"))
async def play_tic_tac_toe(client, callback_query):
    chat_id = int(callback_query.data.split("_")[2])
    position = int(callback_query.data.split("_")[1])
    user_id = callback_query.from_user.id

    # Validate the player's turn
    if game_state[chat_id]['players'][0] == user_id and game_state[chat_id]['turn'] == 'X' or \
       game_state[chat_id]['players'][1] == user_id and game_state[chat_id]['turn'] == 'O':
        board, winner = update_board(chat_id, position)
        if winner:
            await callback_query.message.edit_text(f"{winner} wins!\n{get_board_message(board)}")
            del game_state[chat_id]
        else:
            buttons = [
                [InlineKeyboardButton(str(i), callback_data=f"play_{i}_{chat_id}") if board[i] == ' ' else InlineKeyboardButton(" ", callback_data="disabled") for i in range(3)],
                [InlineKeyboardButton(str(i + 3), callback_data=f"play_{i + 3}_{chat_id}") if board[i + 3] == ' ' else InlineKeyboardButton(" ", callback_data="disabled") for i in range(3)],
                [InlineKeyboardButton(str(i + 6), callback_data=f"play_{i + 6}_{chat_id}") if board[i + 6] == ' ' else InlineKeyboardButton(" ", callback_data="disabled") for i in range(3)]
            ]
            keyboard = InlineKeyboardMarkup(buttons)
            next_turn = game_state[chat_id]['turn']
            await callback_query.message.edit_text(f"Next turn: {next_turn}\n{get_board_message(board)}", reply_markup=keyboard)
    else:
        await callback_query.answer("It's not your turn!", show_alert=True)

# Number Guessing Game
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
