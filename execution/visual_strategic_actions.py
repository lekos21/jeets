from random import choice


def hire_shillers_visual(action_log, phrases_pool):
    full_message = choice(phrases_pool['message']).format(**action_log)
    return full_message

def cex_partnership_visual(action_log, phrases_pool):
    full_message = choice(phrases_pool['message']).format(**action_log)
    return full_message

def burn_tokens_visual(action_log, phrases_pool):
    full_message = choice(phrases_pool['message']).format(**action_log)
    return full_message

def four_visual(action_log, phrases_pool):
    action_log['len(roll_results)'] = action_log['roll_results'].count(True)
    full_message = choice(phrases_pool['message']).format(**action_log)
    return full_message

def hire_hackers_visual(action_log, phrases_pool):
    if action_log['bonus_autism_2'] > 0:
        full_message = choice(phrases_pool['message']).format(**action_log)
    else:
        full_message = choice(phrases_pool['message_fail']).format(**action_log)
    return full_message

def kill_inversebrah_visual(action_log, phrases_pool):
    base_message = choice(phrases_pool['base_message']).format(**action_log)
    if action_log['hype_stolen'] > 0:
        result_message = choice(phrases_pool['result_message']).format(**action_log)
    else:
        result_message = choice(phrases_pool['result_message_fail']).format(**action_log)
    return f"{base_message} {result_message}"