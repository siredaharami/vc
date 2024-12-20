from pyrogram import Client, filters
import random
from BADUC.core.clients import app
from pyrogram import Client
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

# Game state to track the board
game_state = {}

# Tic-Tac-Toe Board
def create_board():
    return [' ' for _ in range(9)]

# Function to check winner
def check_winner(board):
    winning_combinations = [(0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6)]
    for a, b, c in winning_combinations:
        if board[a] == board[b] == board[c] and board[a] != ' ':
            return board[a]
    return None

# Update the board and return message
def update_board(user_id, position):
    board = game_state[user_id]['board']
    if board[position] == ' ':
        board[position] = 'X' if game_state[user_id]['turn'] == 'X' else 'O'
        winner = check_winner(board)
        game_state[user_id]['turn'] = 'O' if game_state[user_id]['turn'] == 'X' else 'X'
        return (board, winner)
    return (board, None)

# Display the board
def get_board_message(board):
    board_str = "\n".join([" | ".join(board[i:i+3]) for i in range(0, 9, 3)])
    return f"Current Board:\n{board_str}"

# Start a new game
@app.on_message(filters.command("startgame"))
async def start_game(client, message):
    user_id = message.from_user.id
    game_state[user_id] = {
        'board': create_board(),
        'turn': 'X',
    }
    buttons = [[InlineKeyboardButton(str(i), callback_data=f"play_{i}") for i in range(3)], 
               [InlineKeyboardButton(str(i+3), callback_data=f"play_{i+3}") for i in range(3)], 
               [InlineKeyboardButton(str(i+6), callback_data=f"play_{i+6}") for i in range(3)]]
    
    keyboard = InlineKeyboardMarkup(buttons)
    await message.reply("Game started! Your turn (X).", reply_markup=keyboard)

# Handle the moves
@app.on_callback_query()
async def on_move(client, callback_query):
    user_id = callback_query.from_user.id
    position = int(callback_query.data.split("_")[1])
    board, winner = update_board(user_id, position)
    
    if winner:
        await callback_query.edit_message_text(f"{winner} wins!\n{get_board_message(board)}")
        game_state.pop(user_id)
    else:
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton(str(i), callback_data=f"play_{i}") for i in range(3)], 
            [InlineKeyboardButton(str(i+3), callback_data=f"play_{i+3}") for i in range(3)], 
            [InlineKeyboardButton(str(i+6), callback_data=f"play_{i+6}") for i in range(3)]
        ])
        await callback_query.edit_message_text(f"Next turn: {game_state[user_id]['turn']}\n{get_board_message(board)}", reply_markup=keyboard)
  
