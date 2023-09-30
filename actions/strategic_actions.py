from basic_functions import *


def hire_shillers_execute(game_data, current_player):
    opponent = 'player1' if current_player == 'player2' else 'player2'

    # Initialize action log
    action_log = {}
    paid_gold = random.randint(12, 18)
    bonus_hype = 15

    # Pay 5 gold to gain 5 hype
    game_data[current_player]['gold'] -= round(paid_gold)
    game_data[current_player]['hype'] += round(bonus_hype)

    # Remove any 'fudded' effects
    fud_removed = False
    for effect_category in ['persistent_effects', 'current_action_effects', 'current_turn_effects',
                            'next_action_effects', 'next_turn_effects']:
        if 'fudded' in game_data[current_player][effect_category]['effects']:
            fud_index = game_data[current_player][effect_category]['effects'].index('fudded')
            del game_data[current_player][effect_category]['effects'][fud_index]
            del game_data[current_player][effect_category]['effects_values'][fud_index]
            fud_removed = True

    action_log.update({
        "label": game_data[current_player]['label'],
        "action": "hire_shillers",
        "paid_gold": paid_gold,
        "bonus_hype": bonus_hype,
        "result": "pending",
        "fud_removed": fud_removed
    })

    # Append the action log to the turns history
    game_data['turns_log'][-1].append(action_log)

    return game_data


def cex_partnership_execute(game_data, current_player):
    # Initialize action log
    action_log = {}

    # Pay 8 gold to gain 2 hype and 2 autism
    gold_paid, hype_gain, autism_gain = 20, 6, 6
    game_data[current_player]['gold'] -= round(gold_paid)
    game_data[current_player]['hype'] += round(hype_gain)
    game_data[current_player]['autism'] += round(autism_gain)

    # Add 'cex_partner' label to persistent effects
    if 'cex_partner' not in game_data[current_player]['persistent_effects']['effects']:
        game_data[current_player]['persistent_effects']['effects'].append('cex_partner')
        game_data[current_player]['persistent_effects']['effects_values'].append(0.35)

    action_log = {
        "label": game_data[current_player]['label'],
        "action": "cex_partnership",
        "gold_spent": gold_paid,
        "hype_gained": hype_gain,
        "autism_gained": autism_gain,
    }

    # Append the action log to the turns history
    game_data['turns_log'][-1].append(action_log)

    return game_data


def burn_tokens_execute(game_data, current_player):
    # Initialize action log
    action_log = {}

    # Deduct 5 gold
    gold_paid = 15
    game_data[current_player]['gold'] -= round(gold_paid)

    # Gain 15-20 hype for the next turn
    hype_gained = random.randint(25, 40)
    game_data[current_player]['next_turn_effects']['hype_modifier'] += round(hype_gained)

    action_log = {
        "label": game_data[current_player]['label'],
        "action": "burn_tokens",
        "gold_spent": gold_paid,
        "next_turn_hype_gained": hype_gained
    }

    # Append the action log to the turns history
    game_data['turns_log'][-1].append(action_log)

    return game_data


def four_execute(game_data, current_player):
    opponent = 'player1' if current_player == 'player2' else 'player2'

    # Initialize action log
    action_log = {}

    initial_gold = game_data[current_player]['gold']
    initial_hype = game_data[current_player]['hype']
    initial_autism = game_data[current_player]['autism']

    # Make player immune from exploits for this turn
    if 'four' not in game_data[opponent]['current_turn_effects']['effects']:
        game_data[current_player]['current_turn_effects']['effects'].append('four')
        game_data[current_player]['current_turn_effects']['effects_values'].append(1)  # 1 means true

    # List to store roll results
    roll_results = []
    gold_spent = 4
    gold_lost = 0
    bonus_hype = 0
    bonus_autism = 0

    # Perform 4 rolls
    for _ in range(4):
        roll_success = dice_roll(44, current_player, game_data)
        roll_results.append(roll_success)
        if roll_success:
            bonus_hype += 4
            bonus_autism += 4
            gold_lost += 4

    game_data[current_player]['gold'] -= round(gold_lost + gold_spent)
    game_data[current_player]['hype'] += round(bonus_hype)
    game_data[current_player]['autism'] += round(bonus_autism)

    action_log = {
        "label": game_data[current_player]['label'],
        "action": "four",
        "gold_spent": gold_spent,
        "roll_results": roll_results,
        "gold_lost": gold_lost,
        "hype_gained": bonus_hype,
        "autism_gained": bonus_autism,
    }

    # Append the action log to the turns history
    game_data['turns_log'][-1].append(action_log)

    return game_data


def hire_hackers_execute(game_data, current_player):
    opponent = 'player1' if current_player == 'player2' else 'player2'

    # Spend 4 gold
    gold_spent = 10
    game_data[current_player]['gold'] -= round(gold_spent)

    # Gain 3 autism
    bonus_autism_1 = 10
    game_data[current_player]['autism'] += round(bonus_autism_1)

    current_hype, current_autism, current_hype_opp, current_autism_opp = get_current_stats(game_data, current_player,
                                                                                           opponent)

    # Check if player has less base autism than opponent
    bonus_autism_2 = 0
    if current_autism < current_autism_opp:
        # Gain 5 base autism
        bonus_autism_2 = random.randint(8, 15)
        game_data[current_player]['autism'] += round(bonus_autism_2)

    action_log = {
        "label": game_data[current_player]['label'],
        "action": "hire_hackers",
        "gold_spent": gold_spent,
        "current_autism": current_autism,
        "current_autism_opp": current_autism_opp,
        "bonus_autism_1": bonus_autism_1,
        "bonus_autism_2": bonus_autism_2,
    }

    # Append the action log to the turns history
    game_data['turns_log'][-1].append(action_log)

    return game_data


def kill_inversebrah_execute(game_data, current_player):
    # Initialize action log
    action_log = {}
    opponent = 'player1' if current_player == 'player2' else 'player2'

    # load current effect and modifiers
    all_current_effects, all_current_values, opponent_current_effects, opponent_current_values = \
        get_effects(game_data, current_player, opponent)

    fudded_value = 0
    if 'fudded' in all_current_effects:
        fudded_index = all_current_effects.index('fudded')
        fudded_value = all_current_values[fudded_index]

    # Gain 3 gold and 2 autism
    gold_gain = 8
    gold_gain_effect_part = round(gold_gain * (-fudded_value))
    autism_gained = 6
    game_data[current_player]['gold'] += round(gold_gain + gold_gain_effect_part)
    game_data[current_player]['autism'] += round(autism_gained)

    opponent = 'player1' if current_player == 'player2' else 'player2'

    current_hype, current_autism, current_hype_opp, current_autism_opp = get_current_stats(game_data,
                                                                                           current_player,
                                                                                           opponent)
    hype_stolen = 0
    # Check if opponent has more gold and hype
    if game_data[current_player]['gold'] < game_data[opponent]['gold'] and \
            current_hype < current_hype_opp:
        # Steal 3 hype from opponent
        hype_stolen = 8
        if hype_stolen > game_data[opponent]['hype']:
            hype_stolen = game_data[opponent]['hype']
            game_data[opponent]['hype'] = 0
            game_data[current_player]['hype'] += hype_stolen

    action_log = {
        "label": game_data[current_player]['label'],
        "action": "kill_inversebrah",
        "current_gold": game_data[current_player]['gold'],
        "current_hype": current_hype,
        "current_gold_opp": game_data[opponent]['gold'],
        "current_hype_opp": current_hype_opp,
        "gold_gained": gold_gain,
        "gold_gained_effects_part": gold_gain_effect_part,
        "autism_gained": autism_gained,
        "hype_stolen": hype_stolen,
    }

    # Append the action log to the turns history
    game_data['turns_log'][-1].append(action_log)

    return game_data
