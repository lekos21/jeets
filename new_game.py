import json
import random
import uuid
from config import *
from execution.macro_actions import send_action_categories
from execution.visual_execution import send_message_to_players
from actions.action_tasks import abandon_game_task

WAITING_PLAYERS_FILE = 'games_data/waiting_players.json'


def new_game_request(chat_id):

    # check if the player had other games currently
    with current_games_lock:
        with open('games_data/current_games.json', 'r') as f:
            current_games = json.load(f)

    # if the user had other games, make it abandon
    if chat_id in current_games:
        abandon_game_task.apply_async(args=[chat_id])


    lock = FileLock(f'{WAITING_PLAYERS_FILE}.lock')
    player1_chat_id = None
    with lock:

        with open(WAITING_PLAYERS_FILE, 'r') as f:
            waiting_players = json.load(f)

        if waiting_players:
            if not str(chat_id) in waiting_players:
                player1_chat_id = waiting_players.pop(0)
            else:
                bot.send_message(chat_id, "You're already waiting for an opponent")
                return
        else:
            markup = InlineKeyboardMarkup()
            markup.row_width = 1
            markup.add(InlineKeyboardButton("❌ Cancel Matchmaking", callback_data=f"exit_matchmaking"))
            bot.send_message(chat_id, f"_You've entered the matchmaking! \nWaiting for a worthy opponent..._",
                             reply_markup=markup, parse_mode='Markdown')
            waiting_players.append(chat_id)

        with open(WAITING_PLAYERS_FILE, 'w') as f:
            json.dump(waiting_players, f, indent=2)

    if player1_chat_id:
        player2_chat_id = chat_id
        start_new_game(player1_chat_id, player2_chat_id)




# Actually start the game
def start_new_game(player1_chat_id, player2_chat_id):

    # copy the "blank" game file and insert players data
    game_data = create_game_json(player1_chat_id, player2_chat_id)

    # Send the initial info
    send_start_game_message(game_data, player1_chat_id, player2_chat_id)

    # Trigger the first turn for player1
    turn = game_data['current_turn']
    send_action_categories(player1_chat_id)
    send_action_categories(player2_chat_id)


def get_username(chat_id):
    lock = FileLock(f'users_data/id_{chat_id}.json.lock')
    with lock:
        with open(f'users_data/id_{chat_id}.json', 'r') as f:
            username = json.load(f)['label']

    return username

def create_game_json(player1_chat_id, player2_chat_id):
    # List existing game files
    existing_files = os.listdir('games_data')
    game_files = [f for f in existing_files if f.startswith('game_') and f.endswith('.json')]

    # Find the highest game number
    highest_number = 0
    for game_file in game_files:
        try:
            number = int(game_file.split('_')[1].split('.')[0])
            highest_number = max(highest_number, number)
        except ValueError:
            continue

    # Create a new game file with the next number
    new_game_number = highest_number + 1
    new_game_file = f'games_data/games_files/game_{new_game_number}.json'
    lock = FileLock(f'{new_game_file}.lock')

    with lock:
        # Generate players stats
        player1_class, player1_stats = generate_random_stats()
        player2_class, player2_stats = generate_random_stats()

        player1_username = get_username(player1_chat_id)
        player2_username = get_username(player2_chat_id)


        with open('games_data/new_game.json', 'r') as f:
            game_data = json.load(f)

        game_data['game_id'] = new_game_number
        game_data['player1']['chat_id'] = player1_chat_id
        game_data['player2']['chat_id'] = player2_chat_id
        game_data['player1']['label'] = player1_username
        game_data['player2']['label'] = player2_username
        game_data['player1']['class'] = player1_class
        game_data['player2']['class'] = player2_class
        game_data['player1'].update(player1_stats)
        game_data['player2'].update(player2_stats)

        with open(new_game_file, 'w') as f:
            json.dump(game_data, f, indent=2)

    # update current games json
    with current_games_lock:
        with open('games_data/current_games.json', 'r') as f:
            current_games = json.load(f)
        current_games[player1_chat_id] = {"game_id": new_game_number, "other_player": player2_chat_id}
        current_games[player2_chat_id] = {"game_id": new_game_number, "other_player": player1_chat_id}

    with open('games_data/current_games.json', 'w') as f:
        json.dump(current_games, f, indent=2)

    return game_data  # Return the name of the new game file if you need it



def generate_random_stats():

    classes = {
        "Threadoor": {"gold": random.randint(16, 22),
                      "hype": random.randint(12, 18),
                      "autism": random.randint(8, 10)},

        "Degen": {"gold": random.randint(5, 8),
                 "hype": random.randint(8, 10),
                 "autism": random.randint(18, 25)},

        "Whale": {"gold": random.randint(25, 30),
                  "hype": random.randint(4, 8),
                  "autism": random.randint(8, 10)},
    }

    chosen_class = random.choice(list(classes.keys()))
    return chosen_class, classes[chosen_class]







def send_start_game_message(game_data, chat_id_1, chat_id_2):
    player1_data = game_data['player1']
    player2_data = game_data['player2']

    general_message = "_Worthy opponent found, let's begin the fight._"
    send_message_to_players(chat_id_1, chat_id_2, general_message)

    stats_msg = f'*{player1_data["label"]}* _({player1_data["class"]})_:\n' \
                   f'🟡*Gold*: {player1_data["gold"]}\n' \
                   f'🔥*Hype*: {player1_data["hype"]}\n' \
                   f'💊*Autism*: {player1_data["autism"]}\n\n' \
                   f'*{player2_data["label"]}* _({player2_data["class"]})_:\n' \
                   f'🟡*Gold*: {player2_data["gold"]}\n' \
                   f'🔥*Hype*: {player2_data["hype"]}\n' \
                   f'💊*Autism*: {player2_data["autism"]}'


    send_message_to_players(chat_id_1, chat_id_2, stats_msg)