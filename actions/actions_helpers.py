import random

from basic_functions import *
from execution.execution import execute_round
from execution.macro_actions import send_action_categories
from execution.visual_execution import show_turn_execution
from actions.mapping_action_label_name import mapping_action_names

def add_pending_action(call, action_name):
    chat_id = call['message']['chat']['id']
    logging.info('getting game id')
    game_id = get_game_id(chat_id)
    game_file = f'games_data/games_files/{game_id}.json'
    lock_game = FileLock(f'{game_file}.lock')

    with lock_game:

        with open(game_file, 'r') as f:
            game_data = json.load(f)
        logging.info('determine player and opponent')
        current_player = 'player1' if str(game_data['player1']['chat_id']) == str(chat_id) else 'player2'
        opponent = 'player2' if current_player == 'player1' else 'player1'

        logging.info('Check if action1 is empty')
        if not game_data['pending_actions']['action1'][current_player]:
            game_data['pending_actions']['action1'][current_player] = action_name
        elif not game_data['pending_actions']['action2'][current_player]:
            game_data['pending_actions']['action2'][current_player] = action_name
        else:
            pass
        # Save the updated game state
        logging.info('Saving move')
        with open(game_file, 'w') as f:
            json.dump(game_data, f, indent=2)

        # Check if current player have filled action1 and action2
        logging.info('Check if action1 and 2 are complete')
        if not (game_data['pending_actions']['action1'][current_player] and game_data['pending_actions']['action2'][
            current_player]):
            logging.info('sending message to user for second action')
            bot.delete_message(chat_id, call['message']['message_id'])
            bot.send_message(chat_id, f"✅ You chose "
                                      f"*{mapping_action_names[game_data['pending_actions']['action1'][current_player]]}*"
                                      f", select your second action.", parse_mode='Markdown')
            send_action_categories(chat_id)
            return

        # Check if opponent have filled action1 and action2
        elif not (game_data['pending_actions']['action1'][opponent] and game_data['pending_actions']['action2'][
            opponent]):
            bot.delete_message(chat_id, call['message']['message_id'])
            bot.send_message(call['message']['chat']['id'],
                             f"Your Actions for this turn:\n"
                             f"1 - *{mapping_action_names[game_data['pending_actions']['action1'][current_player]]}*\n"
                             f"2 - *{mapping_action_names[game_data['pending_actions']['action2'][current_player]]}*",
                             parse_mode='Markdown')
            bot.send_message(call['message']['chat']['id'], f"Waiting for the other player...")
            return

        logging.info(
            f"{game_data['pending_actions']['action1'][current_player]} and {game_data['pending_actions']['action2'][current_player]}")



    # If both players have filled action1 and action2
    if all(game_data['pending_actions']['action1'][player] and game_data['pending_actions']['action2'][player]
           for player in ['player1', 'player2']):
        bot.delete_message(chat_id, call['message']['message_id'])
        bot.send_message(call['message']['chat']['id'],
                         f"Your Actions for this turn:\n"
                         f"1 - *{mapping_action_names[game_data['pending_actions']['action1'][current_player]]}*\n"
                         f"2 - *{mapping_action_names[game_data['pending_actions']['action2'][current_player]]}*",
                         parse_mode='Markdown')
        game_data = execute_round(game_id)
        show_turn_execution(game_data)





def check_if_doxed(call):
    chat_id = str(call['message']['chat']['id'])
    game_id = get_game_id(chat_id)
    game_file = f'games_data/games_files/{game_id}.json'
    lock_game = FileLock(f'{game_file}.lock')

    with lock_game:
        with open(game_file, 'r') as f:
            game_data = json.load(f)

    current_player = 'player1' if game_data['player1']['chat_id'] == chat_id else 'player2'

    if 'doxed' in game_data[current_player]['persistent_effects']['effects']:
        return True
    else:
        return False


def check_if_cex_partner(call):
    chat_id = str(call['message']['chat']['id'])
    game_id = get_game_id(chat_id)
    game_file = f'games_data/games_files/{game_id}.json'
    lock_game = FileLock(f'{game_file}.lock')

    with lock_game:
        with open(game_file, 'r') as f:
            game_data = json.load(f)

    current_player = 'player1' if game_data['player1']['chat_id'] == chat_id else 'player2'

    if 'cex_partner' in game_data[current_player]['persistent_effects']['effects']:
        return True
    else:
        return False
