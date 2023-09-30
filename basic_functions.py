from config import *




def get_game_id(chat_id):

    chat_id = str(chat_id)

    with current_games_lock:
        with open('games_data/current_games.json', 'r') as f:
            current_games = json.load(f)

    if chat_id not in current_games:
        return False  # or raise an exception

    game_id = f"game_{current_games[chat_id]['game_id']}"

    return game_id


def get_current_turn(game_id):
    game_file = f'games_data/games_files/{game_id}.json'
    lock_game = FileLock(f'{game_file}.lock')
    with lock_game:
        with open(game_file, 'r') as f:
            game_data = json.load(f)

    turn = game_data['current_turn']

    return turn

def is_this_turn_callback(call):
    chat_id = call['message']['chat']['id']
    game_id = get_game_id(chat_id)
    current_turn = get_current_turn(game_id)
    callback_turn = call['data'].split("_")[-1]
    if str(current_turn) == str(callback_turn):
        return True
    else:
        return False

def send_message_to_players(chat_id_1, chat_id_2, full_message):
    bot.send_message(chat_id_1, full_message, parse_mode='Markdown')
    bot.send_message(chat_id_2, full_message, parse_mode='Markdown')


def get_effects(game_data, current_player, opponent):
    # Collect all current effects and their values
    all_current_effects = list(set(game_data[current_player]['persistent_effects']['effects'] +
                                   game_data[current_player]['current_turn_effects']['effects'] +
                                   game_data[current_player]['current_action_effects']['effects']))

    all_current_values = game_data[current_player]['persistent_effects']['effects_values'] + \
                         game_data[current_player]['current_turn_effects']['effects_values'] + \
                         game_data[current_player]['current_action_effects']['effects_values']

    opponent_current_effects = list(set(game_data[opponent]['persistent_effects']['effects'] +
                                        game_data[opponent]['current_turn_effects']['effects'] +
                                        game_data[opponent]['current_action_effects']['effects']))

    opponent_current_values = game_data[opponent]['persistent_effects']['effects_values'] + \
                              game_data[opponent]['current_turn_effects']['effects_values'] + \
                              game_data[opponent]['current_action_effects']['effects_values']

    return all_current_effects, all_current_values, opponent_current_effects, opponent_current_values


def get_next_effects(game_data, current_player, opponent):

    # Collect all current effects and their values
    all_next_effects = list(set(game_data[current_player]['persistent_effects']['effects'] +
                                   game_data[current_player]['next_turn_effects']['effects'] +
                                   game_data[current_player]['next_action_effects']['effects']))

    all_next_values = game_data[current_player]['persistent_effects']['effects_values'] + \
                         game_data[current_player]['next_turn_effects']['effects_values'] + \
                         game_data[current_player]['next_action_effects']['effects_values']

    opponent_next_effects = list(set(game_data[opponent]['persistent_effects']['effects'] +
                                        game_data[opponent]['next_turn_effects']['effects'] +
                                        game_data[opponent]['next_action_effects']['effects']))

    opponent_next_values = game_data[opponent]['persistent_effects']['effects_values'] + \
                              game_data[opponent]['next_turn_effects']['effects_values'] + \
                              game_data[opponent]['next_action_effects']['effects_values']

    return all_next_effects, all_next_values, opponent_next_effects, opponent_next_values




def get_current_stats(game_data, current_player, opponent):
    # Base stats
    base_hype = game_data[current_player]['hype']
    base_autism = game_data[current_player]['autism']
    base_hype_opp = game_data[opponent]['hype']
    base_autism_opp = game_data[opponent]['autism']

    # Modifiers for current turn and action
    current_turn_hype_modifier = game_data[current_player]['current_turn_effects']['hype_modifier']
    current_turn_autism_modifier = game_data[current_player]['current_turn_effects']['autism_modifier']
    current_action_hype_modifier = game_data[current_player]['current_action_effects']['hype_modifier']
    current_action_autism_modifier = game_data[current_player]['current_action_effects']['autism_modifier']

    current_turn_hype_modifier_opp = game_data[opponent]['current_turn_effects']['hype_modifier']
    current_turn_autism_modifier_opp = game_data[opponent]['current_turn_effects']['autism_modifier']
    current_action_hype_modifier_opp = game_data[opponent]['current_action_effects']['hype_modifier']
    current_action_autism_modifier_opp = game_data[opponent]['current_action_effects']['autism_modifier']

    # Calculate current stats
    current_hype = base_hype + current_turn_hype_modifier + current_action_hype_modifier
    current_autism = base_autism + current_turn_autism_modifier + current_action_autism_modifier

    current_hype_opp = base_hype_opp + current_turn_hype_modifier_opp + current_action_hype_modifier_opp
    current_autism_opp = base_autism_opp + current_turn_autism_modifier_opp + current_action_autism_modifier_opp

    return current_hype, current_autism, current_hype_opp, current_autism_opp


def clean_current_games_json(chat_id):
    with current_games_lock:
        with open('games_data/current_games.json', 'r') as f:
            current_games = json.load(f)

        if chat_id in current_games:
            del current_games[chat_id]

        with open('games_data/current_games.json', 'w') as f:
            json.dump(current_games, f, indent=2)


def dice_roll(prob, current_player, game_data):
    roll = random.randint(1, 100)
    if roll <= prob:
        return True
    else:
        return False


def serialize_call(call):
    return {
        'data': call.data,
        'message': {
            'message_id': call.message.message_id,
            'chat': {
                'id': call.message.chat.id
            },
            # Add other relevant fields
        },
        # Add other relevant fields
    }