import json
import random
from filelock import FileLock
from config import *
from .visual_resource_actions import *
from .visual_sabotage_actions import *
from .visual_strategic_actions import *
from basic_functions import *
from execution.macro_actions import send_action_categories
from execution.end_of_game import show_end_of_game
from actions.mapping_action_label_name import *



def show_turn_execution(game_data):
    chat_id_1 = game_data['player1']['chat_id']
    chat_id_2 = game_data['player2']['chat_id']

    # Load the message templates
    lock = FileLock('games_data/execution_messages.json.lock')
    with lock:
        with open('games_data/execution_messages.json', 'r') as f:
            message_templates = json.load(f)

    send_message_to_players(chat_id_1, chat_id_2, f"*ROUND {game_data['current_turn']-1} - Execution Phase*")

    turn_log = game_data['turns_log'][-2]           # already added the new one so -2
    logging.info(f"begin loop for actions, turn_log: {turn_log}")
    for action_log in turn_log:
        action_name = action_log['action']
        logging.info(f"{action_name}")
        phrases_pool = message_templates.get(action_name, {})
        logging.info(f"{phrases_pool}")
        # Add the label to the action_log for string formatting

        #CREATE ACTIONS MESSAGES
        logging.info(f"create action messages {action_name}")
        full_message = f"*{action_log['label']}* uses *{mapping_action_names[action_name]}*\n"

        if action_name == 'raise_for_new_L2':
            full_message += raise_for_new_L2_visual(action_log, phrases_pool)
        elif action_name == 'farm_airdrop':
            full_message += farm_airdrop_visual(action_log, phrases_pool)
        elif action_name == 'deploy_memecoin':
            full_message += deploy_memecoin_visual(action_log, phrases_pool)
        elif action_name == 'rug_pull':
            full_message += rug_pull_visual(action_log, phrases_pool)
        elif action_name == 'pump_and_dump':
            full_message += pump_and_dump_visual(action_log, phrases_pool)
        elif action_name == 'stake':
            full_message += stake_visual(action_log, phrases_pool)
        elif action_name == 'exploit_opp':
            full_message += exploit_opp_visual(action_log, phrases_pool)
        elif action_name == 'fud_opp':
            full_message += fud_opp_visual(action_log, phrases_pool)
        elif action_name == 'dox_opp':
            full_message += dox_opp_visual(action_log, phrases_pool)
        elif action_name == 'flash_loan':
            full_message += flash_loan_visual(action_log, phrases_pool)
        elif action_name == 'hire_shillers':
            full_message += hire_shillers_visual(action_log, phrases_pool)
        elif action_name == 'cex_partnership':
            full_message += cex_partnership_visual(action_log, phrases_pool)
        elif action_name == 'burn_tokens':
            full_message += burn_tokens_visual(action_log, phrases_pool)
        elif action_name == 'four':
            full_message += four_visual(action_log, phrases_pool)
        elif action_name == 'hire_hackers':
            full_message += hire_hackers_visual(action_log, phrases_pool)
        elif action_name == 'kill_inversebrah':
            full_message += kill_inversebrah_visual(action_log, phrases_pool)

        # Show action results
        logging.info("sending turn visual execution to the players")
        time.sleep(2)
        send_message_to_players(chat_id_1, chat_id_2, full_message)

    # Show turn recap
    logging.info("show turn recap")
    show_unstake(game_data)
    show_end_of_turn_recap(chat_id_1, chat_id_2, game_data)


def show_unstake(game_data):
    for player in ['player1', 'player2']:
        if game_data[player]['unstaked_this_turn'] > 0:
            chat_id_1 = game_data['player1']['chat_id']
            chat_id_2 = game_data['player2']['chat_id']
            gold_gained_back = game_data[player]['unstaked_this_turn']

            send_message_to_players(chat_id_1, chat_id_2, f"_{game_data[player]['label']} unstaked and "
                                                          f"got {gold_gained_back}🟡 back._")

def show_end_of_turn_recap(chat_id_1, chat_id_2, game_data):



    current_effects1, current_values1, current_effects2, current_values2 = \
        get_next_effects(game_data, 'player1', 'player2')

    # these are CURRENT BECAUSE IT'S END OF TURN, BUT ACTUALLY STILL IN THE "NEXT" SLOTS.
    current_hype_1, current_autism_1, current_hype_2, current_autism_2 = get_current_stats(game_data,
                                                                                           'player1',
                                                                                           'player2')

    bonus_hype1 = current_hype_1 - game_data['player1']['hype']
    bh1_sign = "+" if bonus_hype1 >= 0 else ""
    bonus_hype2 = current_hype_2 - game_data['player2']['hype']
    bh2_sign = "+" if bonus_hype2 >= 0 else ""
    bonus_autism1 = current_autism_1 - game_data['player1']['autism']
    ba1_sign = "+" if bonus_autism1 >= 0 else ""
    bonus_autism2 = current_autism_2 - game_data['player2']['autism']
    ba2_sign = "+" if bonus_autism2 >= 0 else ""

    formatted_list1 = [f"{mapping_effects_names[effect]} ({int(value * 100)}%)" for effect, value in zip(current_effects1, current_values1)]
    effects1 = ', '.join(formatted_list1) if ', '.join(formatted_list1) != '' else '_none_'
    formatted_list2 = [f"{mapping_effects_names[effect]} ({int(value * 100)}%)" for effect, value in zip(current_effects2, current_values2)]
    effects2 = ', '.join(formatted_list2) if ', '.join(formatted_list2) != '' else '_none_'



    next_turn_starter = game_data['player1']['label'] if int(game_data['current_turn'])%2 == 1 else game_data['player1']['label']

    full_message = f'''*ROUND {game_data['current_turn']}: Selection Phase ({next_turn_starter} will start)*
*{game_data['player1']['label']}*:
🟡 *Gold*: {int(game_data['prev_turn_player1']['gold'])} ➡️ {int(game_data['player1']['gold'])}
🔥 *Hype*: {int(game_data['prev_turn_player1']['hype'])} ➡️ {int(game_data['player1']['hype'])} ({bh1_sign}{int(bonus_hype1)}✨)
💊 *Autism*: {int(game_data['prev_turn_player1']['autism'])} ➡️ {int(game_data['player1']['autism'])} ({ba1_sign}{int(bonus_autism1)}✨)
_Effects: {effects1}_

*{game_data['player2']['label']}*:
🟡 *Gold*: {int(game_data['prev_turn_player2']['gold'])} ➡️ {int(game_data['player2']['gold'])} 
🔥 *Hype*: {int(game_data['prev_turn_player2']['hype'])} ➡️ {int(game_data['player2']['hype'])} ({bh2_sign}{int(bonus_hype2)}✨)
💊 *Autism*: {int(game_data['prev_turn_player2']['autism'])} ➡️ {int(game_data['player2']['autism'])} ({ba2_sign}{int(bonus_autism2)}✨)
_Effects: {effects2}_
    '''

    time.sleep(2)
    send_message_to_players(chat_id_1, chat_id_2, full_message)
    new_turn_or_endgame(game_data, chat_id_1, chat_id_2)


def new_turn_or_endgame(game_data, chat_id_1, chat_id_2, abandoned=False):
    if abandoned or game_data["current_turn"] > 6:
        show_end_of_game(game_data)
    else:
        send_action_categories(chat_id_1)
        send_action_categories(chat_id_2)

