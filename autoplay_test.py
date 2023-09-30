'''
this is autoplay function. by pressing play
you will create automatically N games with relative jsons
'''
import json
import random
from actions.resource_actions import *
from actions.sabotage_actions import *
from actions.strategic_actions import *
from actions.mapping_action_label_name import *
from new_game import generate_random_stats
from execution.execution import reset_effects, clear_pending_actions


def end_of_turn_unstake_test(game_data, ordered_player_list):
    for player in ordered_player_list:
        if game_data[player]['staked'] > 0:
            yield_pct = 0
            for action_log in game_data['turns_log'][-1]:
                if action_log['action'] == 'stake':
                    yield_pct = action_log['yield']

            gold_staked = game_data[player]['staked']
            gold_gained_back = round(gold_staked * (1 + yield_pct / 100))

            # Move staked coins and yield back to gold
            game_data[player]['gold'] += round(gold_gained_back)

            # Reset staked amount
            game_data[player]['staked'] = 0

    return game_data

if __name__ == '__main__':


    n = 2

    for i in range(n):

        with open('games_data/new_game.json', 'r') as f:
            game_data = json.load(f)

        game_data['player1']['label'] = 'player1'
        game_data['player2']['label'] = 'player2'

        with open(f'games_data/test_games/game_{i}.json', 'w') as f:
            json.dump(game_data, f, indent=2)

        player1_class, player1_stats = generate_random_stats()
        player2_class, player2_stats = generate_random_stats()

        game_data['player1']['class'] = player1_class
        game_data['player2']['class'] = player2_class
        game_data['player1'].update(player1_stats)
        game_data['player2'].update(player2_stats)
        game_data['initial_stats'] = [player1_stats, player2_stats]

        for turn in range(6):
            # reset turn effects
            for player in ['player1', 'player2']:
                game_data[player]['current_turn_effects'] = game_data[player]['next_turn_effects']
                game_data[player]['next_turn_effects'] = reset_effects()  # Reset to default



            for action_num in range(2):
                for player in ['player1', 'player2']:



                    action_name = random.choice(list(mapping_action_names))

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

                    eoa_stats = {
                        "turn": game_data['current_turn'],
                        "player1": game_data["player1"],
                        "player2": game_data["player2"]
                    }

                    # update last action with current stats
                    game_data['turns_log'][-1][-1]['end_of_action_stats'] = eoa_stats


                    game_data[player]['current_action_effects'] = game_data[player]['next_action_effects']
                    game_data[player]['next_action_effects'] = reset_effects()

            # increment turn
            game_data["current_turn"] += 1

            # create an empty slot for this turn actions
            game_data['turns_log'].append([])

            ordered_player_list = ['player1', 'player2'] if round(game_data['current_turn']) % 2 == 1 else ['player2',
                                                                                                      'player1']
            game_data = end_of_turn_unstake_test(game_data, ordered_player_list)

            game_data = clear_pending_actions(game_data)

        game_data[player]['current_turn_effects'] = game_data[player]['next_turn_effects']
        game_data[player]['next_turn_effects'] = reset_effects()  # Reset to default

        with open(f'games_data/test_games/game_{i}.json', 'w') as f:
            json.dump(game_data, f, indent=2)







