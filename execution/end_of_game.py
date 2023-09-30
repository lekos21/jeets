import time
from config import *
from basic_functions import *

# abandoned should be None, 'player1', 'player2' or 'both'



def show_end_of_game(game_data):
    # Determine winner
    winner_id, loser_id, tie_ids = determine_winner(game_data)

    # Update user info (update BOTH but only returns winner's, needed to send custom message)
    user_info_winner = update_personal_info(winner_id, loser_id)

    # Create personalized messages for loser and winner
    send_endgame_message(game_data, user_info_winner, winner_id, loser_id, tie_ids)

    # clean current_games.json
    clean_current_games_json(game_data['player1']['chat_id'])
    clean_current_games_json(game_data['player2']['chat_id'])


def determine_winner(game_data):

    if game_data['player1']['gold'] == game_data['player2']['gold']:
        winner_id = None
        loser_id = None
        tie_ids = [game_data['player1']['chat_id'], game_data['player2']['chat_id']]
    elif game_data['player1']['gold'] > game_data['player2']['gold']:
        winner_id = game_data['player1']['chat_id']
        loser_id = game_data['player2']['chat_id']
        tie_ids = None
    else:
        winner_id = game_data['player2']['chat_id']
        loser_id = game_data['player1']['chat_id']
        tie_ids = None

    return winner_id, loser_id, tie_ids




def update_personal_info(winner_id, loser_id):
    # Update personal stats
    loser_lock = FileLock(f'users_data/id_{loser_id}.json.lock')
    with loser_lock:
        with open(f'users_data/id_{loser_id}.json', 'r') as f:
            user_info = json.load(f)

        user_info['streak'] = 0
        user_info['loss'] += 1

        with open(f'users_data/id_{loser_id}.json', 'w') as f:
            json.dump(user_info, f, indent=2)

    winner_lock = FileLock(f'users_data/id_{winner_id}.json.lock')
    with winner_lock:
        with open(f'users_data/id_{winner_id}.json', 'r') as f:
            user_info_winner = json.load(f)

        user_info_winner['streak'] += 1
        user_info_winner['win_by_abandon'] += 1

        # update max streak if needed
        if user_info_winner['streak'] > user_info_winner['max_streak']:
            user_info_winner['max_streak'] = user_info_winner['streak']

        with open(f'users_data/id_{winner_id}.json', 'w') as f:
            json.dump(user_info, f, indent=2)
    return user_info_winner



#tie is a list with the 2 chat IDs
def send_endgame_message(game_data, user_info_winner, winner_id=None, loser_id=None, tie=None):
# Retrieves labels
    loser_label = game_data['player1']['label'] if game_data['player1']['chat_id'] == loser_id else \
    game_data['player2']['label']
    winner_label = game_data['player1']['label'] if game_data['player1']['chat_id'] == winner_id else \
        game_data['player2']['label']


    # Common message
    if tie:
        msg = f"Wow, a tie! It's really frustrating for everybody, who the fuck coded this game?\n Do you want to play a /new_game?"
        bot.send_message(tie[0], msg, parse_mode='HTML')
        bot.send_message(tie[1], msg, parse_mode='HTML')
        return

    # Send notification to the players

    loser_gold = game_data['player1']['gold'] if game_data['player1']['gold'] < game_data['player2']['gold'] else game_data['player2']['gold']
    winner_gold = game_data['player1']['gold'] if game_data['player1']['gold'] > game_data['player2']['gold'] else game_data['player2']['gold']

    loser_phrase = random.choice([
        f"Unfortunately, you lost with {loser_gold}🟡 vs {winner_gold}🟡 against {winner_label}. On the bright side, this is just fake money, unlike the ones you're losing IRL.",
        f'{winner_label} destroyed you for {loser_gold}🟡 to {winner_gold}🟡. Your private keys has just been transferred to him.',
        f'''You lost against {winner_label} with {loser_gold}🟡 vs {winner_gold}🟡. Bow down to your new lord.
(•_•)
∫\ \___( •_•)
_∫∫ _∫∫ \ \ 
        
        ''',
        f'Due to unfortunate maket circumstances, you lost {loser_gold}🟡 vs {winner_gold}🟡. Please retry in the bull run.',
        f'Ong you just got smoked 💀. You lost {loser_gold}🟡 to {winner_gold}🟡.',
        f'{winner_label} is a few trading levels above you and won {loser_gold}🟡 to {winner_gold}🟡. You still got much to learn. and that is totally fine. we are all here to learn, improve & help each other.',
        f'You lost {loser_gold}🟡 to {winner_gold}🟡. Your winrate is NOT naturally going down. It is being pushed down via whales placing spoofy sell orders on exchanges to make noobs and risk managers sell to buy back lower. ',
        f'In a jungle watching your game being lost {loser_gold}🟡 to {winner_gold}🟡, you feel nothing. You can keep losing longer than this market can remain irrational. 46k wins is programmed. Stay safe homie.'
    ])

    bot.send_message(loser_id, loser_phrase)


    winner_phrase = random.choice([
        f"You won the match with {winner_gold}🟡 vs {loser_gold}🟡 of your opponent, but you just got liquidated on Binance.",
        f"You won with {winner_gold}🟡 vs {loser_gold}🟡. We had to rig the game a bit for it to happen, but we like you so it's worth it",
        f"OMG!😭Can't believe you won {winner_gold}🟡 vs {loser_gold}🟡! Thank you Walton team ! ❤️ keep doing the great work. 💪🏻💪🏻💪🏻🚀🚀🚀",
        f"You sacrificed everything, and in the end you won {winner_gold}🟡 vs {loser_gold}🟡. You can tell the world you are not a loser.",
        f"In the end, won {winner_gold}🟡 to {loser_gold}🟡. \nPatience.\nDiscipline.\nJingTao."
    ])

    winner_phrase += "\n\n"
    for i in range(user_info_winner['streak']):
        winner_phrase += '🏆'

    bot.send_message(winner_id, f'{winner_phrase}\n\nPlay a /new_game?', parse_mode='HTML')