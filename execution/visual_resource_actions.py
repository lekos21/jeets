from random import choice


def raise_for_new_L2_visual(action_log, phrases_pool):


    # Determine which effects message to use
    effects_key = 'no_effects'
    if action_log['fudded'] > 0 and action_log['cex'] > 0:
        effects_key = 'fudded_and_cex'
    elif action_log['fudded'] > 0:
        effects_key = 'fudded'
    elif action_log['cex'] > 0:
        effects_key = 'cex'

    # Get the effects message and format it
    effects_message = phrases_pool['effects_message'][effects_key].format(**action_log)

    # Add signs for effect contributions
    action_log['fixed_gold_gained_effects_part_sign'] = '+' if action_log['fixed_gold_gained_effects_part'] >= 0 else ''
    action_log['extra_gold_gained_effects_contribution_sign'] = '+' if action_log[
                                                                           'extra_gold_gained_effects_contribution'] >= 0 else ''

    # Get the base gains message and format it
    base_gains_message = choice(phrases_pool['base_gains_message']).format(**action_log)

    # show preroll stats
    action_log['hype_diff'] = action_log['current_hype'] - action_log['current_hype_opp']

    roll_stats_message = choice(phrases_pool['preroll_stats_message']).format(**action_log)

    # Prepare the extra gains message based on roll success
    extra_gains_message = ""
    if action_log['roll_success']:
        extra_gains_message = choice(phrases_pool['extra_gains_message']).format(**action_log)
    else:
        extra_gains_message = choice(phrases_pool['roll_fail_message']).format(**action_log)

    # Combine all messages into one
    full_message = f"_{effects_message}_\n{base_gains_message}\n{roll_stats_message}\n{extra_gains_message}"

    return full_message


def farm_airdrop_visual(action_log, phrases_pool):

    # Determine which effects message to use
    effects_key = 'no_effects'
    if action_log['fudded'] > 0:
        effects_key = 'fudded'

    # Get the effects message and format it
    effects_message = phrases_pool['effects_message'][effects_key].format(**action_log)

    # Add signs for effect contributions
    action_log['gold_gained_effects_part_sign'] = '+' if action_log['gold_gained_effects_part'] >= 0 else '-'

    # Get the base gains message and format it
    base_gains_message = choice(phrases_pool['base_gains_message']).format(**action_log)

    # Combine all messages into one
    full_message = f"_{effects_message}_\n{base_gains_message}"

    return full_message


def deploy_memecoin_visual(action_log, phrases_pool):

    # Determine which effects message to use
    effects_key = 'no_effects'
    if action_log['fudded'] > 0 and action_log['cex'] > 0:
        effects_key = 'fudded_and_cex'
    elif action_log['fudded'] > 0:
        effects_key = 'fudded'
    elif action_log['cex'] > 0:
        effects_key = 'cex'

    # Get the effects message and format it
    effects_message = phrases_pool['effects_message'][effects_key].format(**action_log)

    # show preroll stats
    roll_stats_message = choice(phrases_pool['preroll_stats_message']).format(**action_log)

    # Add signs for effect contributions
    action_log['gold_returned_effects_part_sign'] = '+' if action_log['gold_returned_effects_part'] >= 0 else '-'

    # Get the base gains message and format it
    base_gains_message = choice(phrases_pool['base_gains_message']).format(**action_log)

    # Combine all messages into one
    full_message = f"_{effects_message}_\n{roll_stats_message}\n{base_gains_message}"

    return full_message


def rug_pull_visual(action_log, phrases_pool):
    # Determine which effects message to use
    effects_key = 'no_effects'
    if action_log['fudded'] > 0:
        effects_key = 'fudded'

    # Get the effects message and format it
    effects_message = phrases_pool['effects_message'][effects_key].format(**action_log)

    # Add signs for effect contributions
    action_log['fixed_bonus_gold_raw_effects_contribution_sign'] = '+' if action_log[
                                                                              'fixed_bonus_gold_raw_effects_contribution'] >= 0 else '-'
    action_log['extra_gold_effects_contribution_sign'] = '+' if action_log[
                                                                    'extra_gold_effects_contribution'] >= 0 else '-'

    # Get the base gains message and format it
    base_gains_message = choice(phrases_pool['base_gains_message']).format(**action_log)

    # Get the extra gains message and format it
    action_log['autism_diff'] = action_log['current_autism'] - action_log['current_autism_opp']
    action_log['autism_diff_sign'] = "+" if action_log['autism_diff'] >=0 else ""

    extra_gains_message = choice(phrases_pool['extra_gains_message']).format(**action_log)

    # Determine Zach thread outcome and get the message
    zach_message_key = 'success' if action_log['zach_thread'] else 'fail'
    zach_message = choice(phrases_pool['zach_message'][zach_message_key]).format(**action_log)

    # Combine all messages into one
    full_message = f"_{effects_message}_\n{base_gains_message}\n{extra_gains_message}\n{zach_message}"

    return full_message


def pump_and_dump_visual(action_log, phrases_pool):
    # Determine which effects message to use
    effects_key = 'no_effects'
    if action_log['fudded'] > 0:
        effects_key = 'fudded'

    # Get the effects message and format it
    effects_message = phrases_pool['effects_message'][effects_key].format(**action_log)

    # Add signs for effect contributions
    action_log['gold_gained_effects_contribution_sign'] = '+' if action_log[
                                                                     'gold_gained_effects_contribution'] >= 0 else '-'

    # Get the gains message and format it
    gains_message = choice(phrases_pool['gains_message']).format(**action_log)

    # Determine Zach thread outcome and get the message
    zach_message_key = 'success' if action_log['zach_thread'] else 'fail'
    zach_message = choice(phrases_pool['zach_message'][zach_message_key]).format(**action_log)

    # Combine all messages into one
    full_message = f"_{effects_message}_\n{gains_message}\n{zach_message}"

    return full_message

def stake_visual(action_log, phrases_pool):
    # Get the stake message and format it
    stake_message = choice(phrases_pool['stake_message']).format(**action_log)

    return stake_message