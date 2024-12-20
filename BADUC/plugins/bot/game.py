from pyrogram import Client, filters
from BADUC.core.clients import bot
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

# Game state to track the board and players
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
    board = game_state['board']
    if board[position] == ' ':
        board[position] = 'X' if game_state['turn'] == 'X' else 'O'
        winner = check_winner(board)
        game_state['turn'] = 'O' if game_state['turn'] == 'X' else 'X'
        return (board, winner)
    return (board, None)

# Display the board
def get_board_message(board):
    board_str = "\n".join([" | ".join(board[i:i+3]) for i in range(0, 9, 3)])
    return f"Current Board:\n{board_str}"

# Start a new game
@bot.on_message(filters.command("game"))
async def start_game(client, message):
    user_id = message.from_user.id

    if 'players' not in game_state:
        game_state['players'] = [user_id]  # First player is the user who starts the game
        game_state['turn'] = 'X'
        game_state['board'] = create_board()
        buttons = [[InlineKeyboardButton(str(i), callback_data=f"play_{i}") for i in range(3)], 
                   [InlineKeyboardButton(str(i+3), callback_data=f"play_{i+3}") for i in range(3)], 
                   [InlineKeyboardButton(str(i+6), callback_data=f"play_{i+6}") for i in range(3)]]
        
        keyboard = InlineKeyboardMarkup(buttons)
        await message.reply("Game started! Your turn (X). Please wait for another player to join.", reply_markup=keyboard)
    else:
        if len(game_state['players']) < 2:
            game_state['players'].append(user_id)  # Second player joins
            game_state['turn'] = 'X'  # Reset to X's turn at the start
            buttons = [[InlineKeyboardButton(str(i), callback_data=f"play_{i}") for i in range(3)], 
                       [InlineKeyboardButton(str(i+3), callback_data=f"play_{i+3}") for i in range(3)], 
                       [InlineKeyboardButton(str(i+6), callback_data=f"play_{i+6}") for i in range(3)]]
            
            keyboard = InlineKeyboardMarkup(buttons)
            await message.reply("Second player joined! Your turn (X).", reply_markup=keyboard)
        else:
            await message.reply("Game is already full. Please wait for the next game.")

# Handle the moves
@bot.on_callback_query()
async def on_move(client, callback_query):
    user_id = callback_query.from_user.id

    # Ensure it's the player's turn
    if user_id != game_state['players'][0] and user_id != game_state['players'][1]:
        return  # Ignore move if player is not in the game

    # Check if it is the correct player's turn
    if (game_state['turn'] == 'X' and user_id != game_state['players'][0]) or (game_state['turn'] == 'O' and user_id != game_state['players'][1]):
        await callback_query.answer("It's not your turn!")
        return

    position = int(callback_query.data.split("_")[1])
    board, winner = update_board(user_id, position)
    
    if winner:
        await callback_query.edit_message_text(f"{winner} wins!\n{get_board_message(board)}")
        game_state.clear()  # Reset game state
    else:
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton(str(i), callback_data=f"play_{i}") for i in range(3)], 
            [InlineKeyboardButton(str(i+3), callback_data=f"play_{i+3}") for i in range(3)], 
            [InlineKeyboardButton(str(i+6), callback_data=f"play_{i+6}") for i in range(3)]
        ])
        next_turn_message = f"Next turn: {game_state['turn']}\n{get_board_message(board)}"
        await callback_query.edit_message_text(next_turn_message, reply_markup=keyboard)
