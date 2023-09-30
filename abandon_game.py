import random
import shutil
from config import *


def abandon_game_func(chat_id):
    game_id = None
    # remove the game from current games and retrieve the game ID
    with current_games_lock:
        with open('games_data/current_games.json', 'r') as f:
            current_games = json.load(f)
        if str(chat_id) in current_games:
            try:
                game_id = f'game_{current_games[str(chat_id)]["game_id"]}'
                other_player_id = current_games[str(chat_id)]['other_player']
                if str(chat_id) in current_games:
                    del current_games[str(chat_id)]
                if str(other_player_id) in current_games:
                    del current_games[str(other_player_id)]
            except:
                pass
        with open('games_data/current_games.json', 'w') as f:
            json.dump(current_games, f, indent=2)
    if game_id:
        lock_game = FileLock(f'games_data/games_files/{game_id}.json.lock')
        with lock_game:
            with open(f'games_data/games_files/{game_id}.json', 'r') as f:
                game_data = json.load(f)


        # Update personal stats
        lock_chat_id_abandoner = FileLock(f'users_data/id_{chat_id}.json.lock')
        with lock_chat_id_abandoner:
            with open(f'users_data/id_{chat_id}.json', 'r') as f:
                user_info = json.load(f)

            user_info['streak'] = 0
            user_info['abandoned'] += 1

            with open(f'users_data/id_{chat_id}.json', 'w') as f:
                json.dump(user_info, f, indent=2)

        lock_chat_id_winner = FileLock(f'users_data/id_{other_player_id}.json.lock')
        with lock_chat_id_winner:
            with open(f'users_data/id_{other_player_id}.json', 'r') as f:
                user_info_winner = json.load(f)

            user_info_winner['streak'] += 1
            user_info_winner['win_by_abandon'] += 1

            with open(f'users_data/id_{other_player_id}.json', 'w') as f:
                json.dump(user_info_winner, f, indent=2)


        # Retrieves labels
        abandoning_player_label = game_data['player1']['label'] if game_data['player1']['chat_id'] == chat_id else \
        game_data['player2']['label']
        winner_player_label = game_data['player1']['label'] if game_data['player1']['chat_id'] == other_player_id else \
            game_data['player2']['label']

        # Send notification to the players

        player_phrases_abandoned = random.choice([
            "You chickened out the current game.",
            "You quit the game, you are a larp that uses inspect element.",
            "You left the game. You are a horrible trader. Me and literally everyone else I know use you as a counter indicator.",
            "You left the current game. Maybe your parents were right about you.",
            "You left the game. Hope you're proud of yourself.",
            f"You left the game. Your private key has been sent to {winner_player_label}.",
            f"You left the game. Your NFT (~${round(random.randrange(100,1000)/100, 2)}) have been sent to *{winner_player_label}*.",
            f"You left the game. Your NFT (~${round(random.randrange(100, 1000) / 100, 2)}) have been sent to *{winner_player_label}*."
        ])

        bot.send_message(chat_id, player_phrases_abandoned, parse_mode='Markdown')


        opponent_phrases = random.choice([
        f"Congrats, <b>{abandoning_player_label}</b> was too scared of your ability and quit the game. Hope you don't have the same effect on women.",
        f"<b>{abandoning_player_label}</b> ran together with Trabucco. Luckily, he didn't steal your money too.",
        f"<b>{abandoning_player_label}</b> left the game to focus on BUIDLing.",
        f"<b>{abandoning_player_label}</b> quit the game to focus on himself.",
        f"<b>{abandoning_player_label}</b> saw your onchain history and decided it wasn't worth it, he quit the game.",
        f"Wow, <b>{abandoning_player_label}</b> must be a Cardano dev since he just disappeared.",
        f"<b>{abandoning_player_label}</b> quit to join DPKR called by DegenSpartan.",
        f"<b>{abandoning_player_label}</b> saw your last tweet and left the game.",
        f"Looks like <b>{abandoning_player_label}</b> chickened out.",
        f"<b>{abandoning_player_label}</b> left the game. You must be like the Mike Tyson of retarded telegram game!",
        f"<b>{abandoning_player_label}</b> is not here anymore. He had a date with a girl (a real one).",
    ])

        opponent_phrases += '\n\n'
        for i in range(user_info_winner['streak']):
            opponent_phrases += '🏆'

        bot.send_message(other_player_id, f'{opponent_phrases}\n\nPlay a /new_game?', parse_mode='HTML')


    # if the player was not in a game
    else:
        bot.send_message(chat_id, "_You're not in any game at the moment._", parse_mode='Markdown')