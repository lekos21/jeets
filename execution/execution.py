import random

from actions.resource_actions import *
from actions.strategic_actions import *
from actions.sabotage_actions import *


def execute_round(game_id):
    game_file = f'games_data/games_files/{game_id}.json'
    lock_game = FileLock(f'{game_file}.lock')

    with lock_game:
        with open(game_file, 'r') as f:
            game_data = json.load(f)

        # store prev turn stuff
        game_data = store_prev_turn_stats(game_data)

        # Move next_turn_effects to current_turn_effects
        for player in ['player1', 'player2']:
            game_data[player]['current_turn_effects'] = copy.deepcopy(game_data[player]['next_turn_effects'])
            game_data[player]['next_turn_effects'] = reset_effects()  # Reset to default

        ordered_player_list = ['player1', 'player2'] if int(game_data['current_turn'])%2 == 1 else ['player2', 'player1']


        for action_num in ['action1', 'action2']:
            for player in ordered_player_list:
                # Move next_action_effects to current_action_effects

                game_data[player]['current_action_effects'] = copy.deepcopy(game_data[player]['next_action_effects'])
                game_data[player]['next_action_effects'] = reset_effects()      # Assuming you have a function to reset effects to default

                action_name = game_data['pending_actions'][action_num][player]

                # Resources
                if action_name == 'raise_for_new_L2':
                    game_data = raise_for_new_L2_execute(game_data, player)
                elif action_name == 'farm_airdrop':
                    game_data = farm_airdrop_execute(game_data, player)
                elif action_name == 'deploy_memecoin':
                    game_data = deploy_memecoin_execute(game_data, player)
                elif action_name == 'rug_pull':
                    game_data = rug_pull_execute(game_data, player)
                elif action_name == 'pump_and_dump':
                    game_data = pump_and_dump_execute(game_data, player)
                elif action_name == 'stake':
                    game_data = stake_execute(game_data, player)
                # Sabotage
                elif action_name == 'exploit_opp':
                    game_data = exploit_opp_execute(game_data, player)
                elif action_name == 'fud_opp':
                    game_data = fud_opp_execute(game_data, player)
                elif action_name == 'dox_opp':
                    game_data = dox_opp_execute(game_data, player)
                elif action_name == 'flash_loan':
                    game_data = flash_loan_execute(game_data, player)
                # Strategic
                elif action_name == 'hire_shillers':
                    game_data = hire_shillers_execute(game_data, player)
                elif action_name == 'cex_partnership':
                    game_data = cex_partnership_execute(game_data, player)
                elif action_name == 'burn_tokens':
                    game_data = burn_tokens_execute(game_data, player)
                elif action_name == 'four':
                    game_data = four_execute(game_data, player)
                elif action_name == 'hire_hackers':
                    game_data = hire_hackers_execute(game_data, player)
                elif action_name == 'kill_inversebrah':
                    game_data = kill_inversebrah_execute(game_data, player)


                # apply penalty if gold is negative
                # if int(game_data[player]['gold']) < 0:
                #     game_data[player]['gold'] -= 5

        # Unstake (needed EACH TURN to clean unstaked of the previous turn too, or have double visualization)
        game_data = end_of_turn_unstake(game_data, ordered_player_list)

        # Clear the pending_actions for the next turn
        game_data = clear_pending_actions(game_data)
        logging.info('pending_actions cleared')

        # increment turn
        game_data["current_turn"] += 1

        # create an empty slot for this turn actions
        game_data['turns_log'].append([])

        # Save the updated game state
        with open(game_file, 'w') as f:
            json.dump(game_data, f, indent=2)


        return game_data


def reset_effects():
    return {
        "hype_modifier": 0,
        "autism_modifier": 0,
        "effects": [],
        "effects_values": []
    }


def clear_pending_actions(game_data):
    game_data['pending_actions'] = {
        "action1": {
            "player1": "",
            "player2": ""
        },
        "action2": {
            "player1": "",
            "player2": ""
        }
    }
    return game_data


def end_of_turn_unstake(game_data, ordered_player_list):
    for player in ordered_player_list:
        # reset unstaked this turn
        game_data[player]['unstaked_this_turn'] = 0
        if game_data[player]['staked'] > 0:
            yield_pct = 0

            # need a loop because he could have staked in 1st or 2nd action. just used to take yield value
            for action_log in game_data['turns_log'][-1]:
                if action_log['action'] == 'stake':
                    yield_pct = action_log['yield']

            gold_staked = game_data[player]['staked']
            gold_gained_back = int(gold_staked * (1 + yield_pct / 100))

            # Move staked coins and yield back to gold
            game_data[player]['gold'] += int(gold_gained_back)

            # save the unstaked number (WITH GAINS) for visualization
            game_data[player]['unstaked_this_turn'] = int(gold_gained_back)

            # Reset staked amount
            game_data[player]['staked'] = 0

            chat_id_1 = game_data['player1']['chat_id']
            chat_id_2 = game_data['player2']['chat_id']


    return game_data






def store_prev_turn_stats(game_data):

    game_data['prev_turn_player1'] = copy.deepcopy(game_data['player1'])
    game_data['prev_turn_player2'] = copy.deepcopy(game_data['player2'])

    return game_data


