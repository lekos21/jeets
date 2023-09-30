from random import choice


def exploit_opp_visual(action_log, phrases_pool):
    # Preliminary message showing autism difference and probability


    preliminary_message = choice(phrases_pool['preliminary_message']).format(**action_log)


    # Check if the exploit was successful
    if action_log['roll_result'] == 'executed':
        # Get the success message and format it
        exploit_message = choice(phrases_pool['success_message']).format(**action_log)
    else:
        # Get the fail message and format it
        exploit_message = choice(phrases_pool['fail_message']).format(**action_log)

    # Combine preliminary and main messages
    full_message = f"{preliminary_message}\n{exploit_message}"

    return full_message


def fud_opp_visual(action_log, phrases_pool):
    # Preliminary message showing hype difference
    action_log['hype_diff'] = action_log['current_hype'] - action_log['current_hype_opp']
    preliminary_message = choice(phrases_pool['preliminary_message']).format(**action_log)

    # Get the success message and format it
    fud_message = choice(phrases_pool['success_message']).format(**action_log)

    # Get the hype spent message and format it
    hype_spent_message = choice(phrases_pool['hype_spent_message']).format(**action_log)

    # Combine preliminary and main messages
    full_message = f"{preliminary_message}\n{fud_message}\n{hype_spent_message}"

    return full_message


def dox_opp_visual(action_log, phrases_pool):
    # Preliminary message showing autism difference
    preliminary_message = choice(phrases_pool['preliminary_message']).format(**action_log)

    # Check if the roll was successful
    if action_log['roll_result']:
        # Get the success message and format it
        dox_message = choice(phrases_pool['success_message']).format(**action_log)
    else:
        # Get the failure message and format it
        dox_message = choice(phrases_pool['failure_message']).format(**action_log)

    # Combine preliminary and main messages
    full_message = f"{preliminary_message}\n{dox_message}"

    return full_message


def flash_loan_visual(action_log, phrases_pool):
    # Check if gold was stolen from the opponent
    if action_log['gold_stolen'] > 0:
        full_message = choice(phrases_pool['success_message']).format(**action_log)
    else:
        full_message = choice(phrases_pool['failure_message']).format(**action_log)

    return full_message