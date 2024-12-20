from pyrogram import Client, filters
import random
from BADUC.core.clients import bot
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, InlineQueryResultArticle, InputTextMessageContent


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

# Inline Query handling
@bot.on_inline_query()
async def inline_query_handler(client, inline_query):
    results = [
        InlineQueryResultArticle(
            title="Tic Tac Toe",
            input_message_content=InputTextMessageContent("Let's play Tic Tac Toe! Click Play to start."),
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("Play", callback_data="tic_tac_toe")]
            ])
        ),
        InlineQueryResultArticle(
            title="Rock, Paper, Scissors",
            input_message_content=InputTextMessageContent("Let's play Rock, Paper, Scissors! Click Play to start."),
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("Play", callback_data="rps")]
            ])
        ),
    ]
    await inline_query.answer(results)

# Start Tic-Tac-Toe Game
@bot.on_callback_query(filters.regex("tic_tac_toe"))
async def start_tic_tac_toe(client, callback_query):
    user_id = callback_query.from_user.id
    game_state[user_id] = {'board': create_board(), 'turn': 'X', 'players': [callback_query.from_user.id, None]}

    # Ensure callback_query.message is available
    if callback_query.message:
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton(str(i), callback_data=f"play_{i}_{user_id}") for i in range(3)],
            [InlineKeyboardButton(str(i + 3), callback_data=f"play_{i + 3}_{user_id}") for i in range(3)],
            [InlineKeyboardButton(str(i + 6), callback_data=f"play_{i + 6}_{user_id}") for i in range(3)]
        ])
        try:
            await callback_query.message.edit_text("Game started! Your turn (X).", reply_markup=keyboard)
        except Exception as e:
            # If edit fails, acknowledge with error message
            await callback_query.answer("Something went wrong. Please try again.")
            print(f"Error editing message: {e}")
    else:
        # If no message exists, inform the user
        await callback_query.answer("Message is not available. Something went wrong.")

# Play Tic-Tac-Toe
@bot.on_callback_query(filters.regex("play_"))
async def play_tic_tac_toe(client, callback_query):
    user_id = callback_query.from_user.id
    position = int(callback_query.data.split("_")[1])
    current_user = int(callback_query.data.split("_")[2])

    # Ensure only the current player can play
    if current_user != user_id:
        await callback_query.answer("It's not your turn!", show_alert=True)
        return

    board, winner = update_board(user_id, position)
    
    # Check winner
    if winner:
        if callback_query.message:
            try:
                await callback_query.message.edit_text(f"{winner} wins!\n{get_board_message(board)}")
            except Exception as e:
                await callback_query.answer("Something went wrong. Please try again.")
                print(f"Error editing message: {e}")
        del game_state[user_id]
    else:
        # Update the game state and show next player's turn
        next_turn = game_state[user_id]['turn']
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton(str(i), callback_data=f"play_{i}_{user_id}") for i in range(3)],
            [InlineKeyboardButton(str(i + 3), callback_data=f"play_{i + 3}_{user_id}") for i in range(3)],
            [InlineKeyboardButton(str(i + 6), callback_data=f"play_{i + 6}_{user_id}") for i in range(3)]
        ])
        if callback_query.message:
            try:
                await callback_query.message.edit_text(f"Next turn: {next_turn}\n{get_board_message(board)}", reply_markup=keyboard)
            except Exception as e:
                await callback_query.answer("Something went wrong. Please try again.")
                print(f"Error editing message: {e}")

# Start Rock, Paper, Scissors
@bot.on_callback_query(filters.regex("rps"))
async def start_rps_game(client, callback_query):
    buttons = [
        [InlineKeyboardButton("Rock", callback_data="rps_rock"),
         InlineKeyboardButton("Paper", callback_data="rps_paper"),
         InlineKeyboardButton("Scissors", callback_data="rps_scissors")]
    ]
    keyboard = InlineKeyboardMarkup(buttons)
    
    if callback_query.message:
        try:
            await callback_query.message.edit_text("Choose Rock, Paper, or Scissors:", reply_markup=keyboard)
        except Exception as e:
            await callback_query.answer("Something went wrong. Please try again.")
            print(f"Error editing message: {e}")
    else:
        await callback_query.answer("Message is not available. Something went wrong.")

# Play Rock, Paper, Scissors
@bot.on_callback_query(filters.regex("rps_"))
async def play_rps(client, callback_query):
    user_choice = callback_query.data.split("_")[1]
    result = play_rps(user_choice)
    
    if callback_query.message:
        try:
            await callback_query.message.edit_text(result)
        except Exception as e:
            await callback_query.answer("Something went wrong. Please try again.")
            print(f"Error editing message: {e}")
    else:
        await callback_query.answer("Message is not available. Something went wrong.")
