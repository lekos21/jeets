from basic_functions import *


def exploit_opp_execute(game_data, current_player):
    opponent = 'player1' if current_player == 'player2' else 'player2'

    current_hype, current_autism, current_hype_opp, current_autism_opp = get_current_stats(game_data, current_player,
                                                                                           opponent)

    # Calculate the percentage of resources to steal based on autism difference
    autism_diff = current_autism - current_autism_opp
    steal_probability = 19.5 + round((autism_diff / 36) * 70)  # Scale linearly
    steal_probability = min(99.5, steal_probability)  # Cap at 99.5%

    # Calculate the resources to steal and update both players
    roll_result = dice_roll(steal_probability, current_player, game_data)
    resources_stolen = round(game_data[opponent]['gold'] * 0.25)

    # initialize hype lost
    hype_lost = 0
    if roll_result:
        game_data[current_player]['gold'] += round(resources_stolen)
        game_data[opponent]['gold'] -= round(resources_stolen)

        # Reduce opponent's hype by 2
        hype_lost = random.randint(3, 9)
        if round(hype_lost) > game_data[opponent]['hype']:
            hype_lost = game_data[opponent]['hype']
            game_data[opponent]['hype'] = 0
        else:
            game_data[opponent]['hype'] -= round(hype_lost)


    # Update the turns history
    action_log = {
        "label": game_data[current_player]['label'],
        "action": "exploit_opp",
        "probability": round(steal_probability),
        "current_autism": current_autism,
        "current_autism_opp": current_autism_opp,
        "roll_result": roll_result,
        "steal_percentage": steal_probability,
        "resources_stolen": resources_stolen,
        "opponent_hype_lost": hype_lost
    }

    game_data['turns_log'][-1].append(action_log)

    return game_data





def fud_opp_execute(game_data, current_player):
    opponent = 'player1' if current_player == 'player2' else 'player2'

    current_hype, current_autism, current_hype_opp, current_autism_opp = get_current_stats(game_data,
                                                                                           current_player,
                                                                                           opponent)
    # Calculate the hype difference
    hype_diff = max(0, current_hype - current_hype_opp)


    # Calculate the resource reduction percentage based on hype difference
    resource_reduction = 0.2 + (hype_diff / 24) * 0.3  # Scale linearly
    resource_reduction = min(0.5, resource_reduction)  # Cap at 50%

    # Calculate the gold loss for the opponent
    gold_loss = round(6 + (hype_diff / 24) * 18)  # Scale linearly
    gold_loss = min(24, gold_loss)  # Cap at 8

    # Update opponent's gold and apply the 'fudded' effect
    game_data[opponent]['gold'] -= gold_loss

    if 'fudded' not in game_data[opponent]['next_turn_effects']['effects']:
        game_data[opponent]['next_turn_effects']['effects'].append('fudded')
        game_data[opponent]['next_turn_effects']['effects_values'].append(resource_reduction)


    # Spend hype from the current player
    hype_lost = 9
    if round(hype_lost) > game_data[current_player]['hype']:
        hype_lost = game_data[current_player]['hype']
        game_data[current_player]['hype'] = 0
    else:
        game_data[current_player]['hype'] -= round(hype_lost)

    # Update the turns history
    action_log = {
        "label": game_data[current_player]['label'],
        "action": "fud_opp",
        "current_hype": current_hype,
        "current_hype_opp": current_hype_opp,
        "resource_reduction": round(resource_reduction*100),
        "gold_loss_for_opponent": gold_loss,
        "hype_spent": hype_lost
    }
    game_data['turns_log'][-1].append(action_log)

    return game_data





def dox_opp_execute(game_data, current_player):
    opponent = 'player1' if current_player == 'player2' else 'player2'

    # opp lose hype
    hype_lost_opp = 6
    if round(hype_lost_opp) > game_data[current_player]['hype']:
        hype_lost_opp = game_data[opponent]['hype']
        game_data[opponent]['hype'] = 0
    else:
        game_data[opponent]['hype'] -= round(hype_lost_opp)

    current_hype, current_autism, current_hype_opp, current_autism_opp = get_current_stats(game_data, current_player,
                                                                                           opponent)

    # Calculate the autism difference
    autism_diff = current_autism - current_autism_opp

    # Calculate the probability based on autism difference
    prob = round(33 + max(0, (autism_diff / 24) * 66.5))  # Scale linearly
    prob = min(99.4, prob)  # Cap at 99%

    # Roll the dice
    roll_result = dice_roll(prob, current_player, game_data)

    if roll_result:
        # Update opponent's hype and apply the 'doxed' effect
        if 'doxed' not in game_data[opponent]['persistent_effects']['effects']:
            game_data[opponent]['persistent_effects']['effects'].append('doxed')
            game_data[opponent]['persistent_effects']['effects_values'].append(1)  # Placeholder value

    # Update the turns history
    action_log = {
        "label": game_data[current_player]['label'],
        "action": "dox_opp",
        "current_autism": current_autism,
        "current_autism_opp": current_autism_opp,
        "probability": round(prob),
        "roll_result": roll_result,
        "hype_loss_for_opponent": hype_lost_opp,
        "effect_applied": "doxed",
    }

    game_data['turns_log'][-1].append(action_log)

    return game_data




def flash_loan_execute(game_data, current_player):
    # Initialize action log
    action_log = {}

    opponent = 'player1' if current_player == 'player2' else 'player2'

    initial_gold = game_data[current_player]['gold']
    initial_gold_opp = game_data[opponent]['gold']

    # Gain 10 gold upfront
    gains_gold = 25
    game_data[current_player]['gold'] += round(gains_gold)

    # Check if you have less gold than your opponent
    stolen_gold = 0
    if game_data[current_player]['gold'] < game_data[opponent]['gold']:
        # Steal 10 gold from opponent
        stolen_gold = 20
        game_data[opponent]['gold'] -= round(stolen_gold)
        game_data[current_player]['gold'] += round(stolen_gold)

    # Pay back 8 gold
    payback_gold = 26
    game_data[current_player]['gold'] -= payback_gold

    action_log.update({
        "label": game_data[current_player]['label'],
        "action": "flash_loan",
        "initial_gold": initial_gold,
        "initial_gold_opp": initial_gold_opp,
        "gold_gained": gains_gold,
        "gold_stolen": stolen_gold,
        "gold_paid_back": payback_gold,
    })

    # Append the action log to the turns history
    game_data['turns_log'][-1].append(action_log)

    return game_data
