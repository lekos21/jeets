from basic_functions import *


def raise_for_new_L2_execute(game_data, current_player):
    opponent = 'player1' if current_player == 'player2' else 'player2'

    # Initialize action log
    action_log = {}

    initial_gold = game_data[current_player]['gold']
    initial_hype = game_data[current_player]['hype']

    # load current effect and modifiers
    all_current_effects, all_current_values, opponent_current_effects, opponent_current_values = \
        get_effects(game_data, current_player, opponent)

    # gain 2 hype and 4 gold BEFORE loading current
    bonus_hype = 3
    game_data[current_player]['hype'] += bonus_hype

    current_hype, current_autism, current_hype_opp, current_autism_opp = get_current_stats(game_data, current_player,
                                                                                           opponent)

    fudded_value = 0
    if 'fudded' in all_current_effects:
        fudded_index = all_current_effects.index('fudded')
        fudded_value = all_current_values[fudded_index]

    cex_value = 0
    if 'cex_partner' in all_current_effects:
        cex_index = all_current_effects.index('cex_partner')
        cex_value = all_current_values[cex_index]

    # add the fixed part with the relative effects
    fixed_gold_raw = 15
    fixed_gold_effects_contribution = fixed_gold_raw * (cex_value - fudded_value)
    game_data[current_player]['gold'] += fixed_gold_raw + fixed_gold_effects_contribution

    # add variable part
    hype_diff = current_hype - current_hype_opp
    hype_diff = min(24, hype_diff)
    hype_diff = max(0, hype_diff)
    prob = 0 + hype_diff / 24 * 60

    # Roll the dice
    roll_success = dice_roll(prob, current_player, game_data)

    extra_gold_gained_raw = 0
    extra_gold_gained_effects_contribution = 0
    if roll_success:
        # Success! Calculate the gold porounds gained
        extra_gold_gained_raw = random.randint(12, 24)

        extra_gold_gained_effects_contribution = extra_gold_gained_raw * (cex_value - fudded_value)

        # Update the player's gold
        game_data[current_player]['gold'] += extra_gold_gained_raw + extra_gold_gained_effects_contribution

        roll_result = "successful"

    else:
        # Failure
        roll_result = "failed"

    action_log.update({
        "label": game_data[current_player]['label'],
        "action": "raise_for_new_L2",
        "initial_gold": initial_gold,
        "initial_hype": initial_hype,
        "fixed_gold_gained": fixed_gold_raw,
        "fixed_gold_gained_effects_part": round(fixed_gold_effects_contribution),
        "fixed_hype_gained": bonus_hype,
        "current_hype": current_hype,
        "current_hype_opp": current_hype_opp,
        "probability": round(prob),
        "roll_success": roll_success,
        "extra_gold_gained_raw": round(extra_gold_gained_raw),  # is 0 if roll fail
        "extra_gold_gained_effects_contribution": round(extra_gold_gained_effects_contribution),
        "fudded": round(fudded_value*100),
        "cex": round(cex_value*100),
        "total_gold_gained_post_effects": fixed_gold_raw + fixed_gold_effects_contribution + \
                                          extra_gold_gained_raw + extra_gold_gained_effects_contribution
    })

    # Append the action log to the turns history
    game_data['turns_log'][-1].append(action_log)

    return game_data





def farm_airdrop_execute(game_data, current_player):
    # Initialize action log
    action_log = {}

    opponent = 'player1' if current_player == 'player2' else 'player2'

    initial_gold = game_data[current_player]['gold']
    initial_hype = game_data[current_player]['hype']

    all_current_effects, all_current_values, opponent_current_effects, opponent_current_values = \
        get_effects(game_data, current_player, opponent)

    fudded_value = 0
    if 'fudded' in all_current_effects:
        fudded_index = all_current_effects.index('fudded')
        fudded_value = all_current_values[fudded_index]

    # Gain 5-10 gold
    gold_gained_raw = random.randint(9, 24)
    gold_gained_effects_part = gold_gained_raw * (-fudded_value)
    game_data[current_player]['gold'] += gold_gained_raw + gold_gained_effects_part

    # Gain autism
    autism_gained = random.randint(3, 6)
    game_data[current_player]['autism'] += autism_gained

    action_log.update({
        "label": game_data[current_player]['label'],
        "action": "farm_airdrop",
        "initial_gold": initial_gold,
        "initial_autism": initial_gold,
        "gold_gained_raw": round(gold_gained_raw),
        "fudded": round(fudded_value*100),
        "gold_gained_effects_part": round(gold_gained_effects_part),
        "autism_gained": autism_gained,
    })

    # Append the action log to the turns history
    game_data['turns_log'][-1].append(action_log)

    return game_data




def deploy_memecoin_execute(game_data, current_player):
    # Initialize action log
    action_log = {}

    opponent = 'player1' if current_player == 'player2' else 'player2'

    initial_gold = game_data[current_player]['gold']
    initial_hype = game_data[current_player]['hype']

    all_current_effects, all_current_values, opponent_current_effects, opponent_current_values = \
        get_effects(game_data, current_player, opponent)

    current_hype, current_autism, current_hype_opp, current_autism_opp = get_current_stats(game_data, current_player,
                                                                                           opponent)

    # define fud
    fudded_value = 0
    if 'fudded' in all_current_effects:
        fudded_index = all_current_effects.index('fudded')
        fudded_value = all_current_values[fudded_index]
        action_log['fudded'] = fudded_value

    cex_value = 0
    if 'cex_partner' in all_current_effects:
        cex_index = all_current_effects.index('cex_partner')
        cex_value = all_current_values[cex_index]

    # Take 70% of player's current gold and put it in LP
    gold_in_LP = round(game_data[current_player]['gold'] * 0.7)
    game_data[current_player]['gold'] -= round(gold_in_LP)

    # Calculate the hype modifier
    hype_modifier = current_hype * 0.0033  # 0.33% improvement per hype poround

    # Randomly get back 75-150% on the LP, improved by hype
    min_pct = 0.8
    max_pct = 1.1
    random_percentage = random.uniform(min_pct, max_pct)
    random_percentage += hype_modifier  # Improve by hype

    gold_returned_raw = round(gold_in_LP * random_percentage)

    gains_made = False
    gold_returned_effects_part = 0
    if gold_returned_raw > gold_in_LP:
        gains_made = True
        gold_returned_effects_part = round((gold_returned_raw - gold_in_LP) * (-fudded_value + cex_value))

    # Update the player's gold
    game_data[current_player]['gold'] += round(gold_returned_raw + gold_returned_effects_part)

    action_log.update({
        "label": game_data[current_player]['label'],
        "action": "deploy_memecoin",
        "initial_gold": initial_gold,
        "initial_hype": initial_hype,
        "base_min_pct": round(min_pct*100),
        "base_max_pct": round(max_pct*100),
        "bonus_pct": round(hype_modifier*100),
        "current_hype": current_hype,
        "gold_in_LP": gold_in_LP,
        "gold_returned_raw": gold_returned_raw,
        "gains_made": gains_made,
        "gold_returned_effects_part": gold_returned_effects_part,
        "fudded": round(fudded_value*100),
        "cex": round(cex_value*100)
    })

    # Append the action log to the turns history
    game_data['turns_log'][-1].append(action_log)

    return game_data





def rug_pull_execute(game_data, current_player):
    # Initialize action log
    action_log = {}

    opponent = 'player1' if current_player == 'player2' else 'player2'

    initial_gold = game_data[current_player]['gold']
    initial_autism = game_data[current_player]['autism']

    all_current_effects, all_current_values, opponent_current_effects, opponent_current_values = \
        get_effects(game_data, current_player, opponent)

    # add autism before loading current
    bonus_autism = 6
    game_data[current_player]['autism'] += round(bonus_autism)

    current_hype, current_autism, current_hype_opp, current_autism_opp = get_current_stats(game_data, current_player,
                                                                                           opponent)

    # define fud
    fudded_value = 0
    if 'fudded' in all_current_effects:
        fudded_index = all_current_effects.index('fudded')
        fudded_value = all_current_values[fudded_index]

    # Gain base 5 gold
    fixed_bonus_gold_raw = 15
    fixed_bonus_gold_raw_effects_contribution = fixed_bonus_gold_raw * (-fudded_value)
    game_data[current_player]['gold'] += round(fixed_bonus_gold_raw + fixed_bonus_gold_raw_effects_contribution)

    # Calculate autism difference and scale extra gold linearly
    autism_diff = current_autism - current_autism_opp
    autism_diff = max(0, min(24, autism_diff))  # Clamp between 0 and 24
    extra_gold_raw = (autism_diff / 24) * 16  # Scale linearly
    extra_gold_effects_contribution = extra_gold_raw * (- fudded_value)

    # Update the player's gold
    game_data[current_player]['gold'] += round(extra_gold_raw + extra_gold_effects_contribution)

    # Roll the dice for a 20% chance of 'zach_thread'
    zach_thread = False
    zach_values = []
    if random.randint(1, 100) <= 20:
        zach_thread = True
        zach_values = [random.randint(7, 12), random.randint(7, 12)]
        game_data[current_player]['gold'] -= round(zach_values[0])
        if round(zach_values[1]) > game_data[current_player]['hype']:
            zach_values[1] = game_data[current_player]['hype']
            game_data[current_player]['hype'] = 0
        else:
            game_data[current_player]['hype'] -= round(zach_values[1])


    action_log.update({
        "label": game_data[current_player]['label'],
        "action": "rug_pull",
        "initial_gold": initial_gold,
        "initial_autism": initial_autism,
        "bonus_autism": round(bonus_autism),
        "current_autism": current_autism,
        "current_autism_opp": current_autism_opp,
        "fudded": round(fudded_value*100),
        "fixed_bonus_gold_raw": round(fixed_bonus_gold_raw),
        "fixed_bonus_gold_raw_effects_contribution": round(fixed_bonus_gold_raw_effects_contribution),
        "extra_gold_raw": round(extra_gold_raw),
        "extra_gold_effects_contribution": round(extra_gold_effects_contribution),
        "zach_thread": zach_thread,
        "zach_values": zach_values
    })

    # Append the action log to the turns history
    game_data['turns_log'][-1].append(action_log)

    return game_data





def pump_and_dump_execute(game_data, current_player):
    opponent = 'player1' if current_player == 'player2' else 'player2'

    all_current_effects, all_current_values, opponent_current_effects, opponent_current_values = \
        get_effects(game_data, current_player, opponent)

    current_hype, current_autism, current_hype_opp, current_autism_opp = get_current_stats(game_data, current_player,
                                                                                           opponent)

    # define fud
    fudded_value = 0
    if 'fudded' in all_current_effects:
        fudded_index = all_current_effects.index('fudded')
        fudded_value = all_current_values[fudded_index]

    # Calculate gold gain based on hype difference
    hype_diff = max(0, current_hype - current_hype_opp)
    gold_gained_raw = 12 + round((hype_diff / 24) * 24)  # Scale linearly
    gold_gained_raw = min(36, gold_gained_raw)  # Cap at 36

    # apply fud
    gold_gained_effects_contribution = round(gold_gained_raw * (- fudded_value))

    # Update the player's gold
    game_data[current_player]['gold'] += round(gold_gained_raw + gold_gained_effects_contribution)

    # Roll the dice for a 20% chance of 'zach_thread'
    zach_thread = False
    zach_values = []
    if random.randint(1, 100) <= 20:
        zach_thread = True
        zach_values = [random.randint(7, 12), random.randint(7, 12)]
        game_data[current_player]['gold'] -= round(zach_values[0])
        if round(zach_values[1]) > game_data[current_player]['hype']:
            zach_values[1] = game_data[current_player]['hype']
            game_data[current_player]['hype'] = 0
        else:
            game_data[current_player]['hype'] -= round(zach_values[1])


    action_log = {
        "label": game_data[current_player]['label'],
        "action": "pump_and_dump",
        "base_hype": game_data[current_player]['hype'],
        "current_hype": current_hype,
        "base_hype_opp": game_data[opponent]['hype'],
        "current_hype_opp": current_hype_opp,
        "hype_diff": int(current_hype - current_hype_opp),
        "gold_gained_effects_contribution": gold_gained_effects_contribution,
        "gold_gained_raw": gold_gained_raw,
        "zach_thread": zach_thread,
        "zach_values": zach_values,
        "fudded": round(fudded_value*100),
    }

    # Update the turns history
    game_data['turns_log'][-1].append(action_log)

    return game_data




def stake_execute(game_data, current_player):
    opponent = 'player1' if current_player == 'player2' else 'player2'
    # Initialize action log

    all_current_effects, all_current_values, opponent_current_effects, opponent_current_values = \
        get_effects(game_data, current_player, opponent)

    initial_gold = round(game_data[current_player]['gold'])

    # Calculate 40% of current gold
    gold_staked = round(game_data[current_player]['gold'] * 0.4)

    # Move 50% of gold to 'staked'
    game_data[current_player]['gold'] -= round(gold_staked)
    game_data[current_player]['staked'] += round(gold_staked)

    # define fud
    fudded_value = 0
    if 'fudded' in all_current_effects:
        fudded_index = all_current_effects.index('fudded')
        fudded_value = all_current_values[fudded_index]

    # Update action log
    action_log = {
        "label": game_data[current_player]['label'],
        "action": "stake",
        "initial_gold": initial_gold,
        "gold_staked": gold_staked,
        "yield": 25,
        "fudded": round(fudded_value * 100),
    }

    # Append the action log to the turns history
    game_data['turns_log'][-1].append(action_log)

    return game_data
