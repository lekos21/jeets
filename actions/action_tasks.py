from actions.actions_helpers import add_pending_action, check_if_doxed, check_if_cex_partner
from config import *
from celery import Celery
from basic_functions import serialize_call
from abandon_game import abandon_game_func

callback_execution = Celery('callbacks', backend='redis://localhost:6379/0', broker='redis://localhost:6379/0')


@callback_execution.task(bind=True)
def raise_for_new_L2_callback_task(self, call):
    add_pending_action(call, 'raise_for_new_L2')


@callback_execution.task(bind=True)
def farm_airdrop_callback_task(self, call):
    add_pending_action(call, 'farm_airdrop')


@callback_execution.task(bind=True)
def deploy_memecoin_callback_task(self, call):
    add_pending_action(call, 'deploy_memecoin')


@callback_execution.task(bind=True)
def rug_pull_callback_task(self, call):
    if not check_if_doxed(call):
        if not check_if_cex_partner(call):
            add_pending_action(call, 'rug_pull')
        elif check_if_cex_partner(call):
            bot.send_message(call['message']['chat']['id'], "❌ You are a CEX partner, you can't rug pull.")
    else:
        bot.send_message(call['message']['chat']['id'], "❌ You are doxed, you can't rug pull.")


@callback_execution.task(bind=True)
def pump_and_dump_callback_task(self, call):
    if not check_if_doxed(call):
        add_pending_action(call, 'pump_and_dump')
    else:
        bot.send_message(call['message']['chat']['id'], "❌ You are doxed, you can't pump and dump.")


@callback_execution.task(bind=True)
def stake_callback_task(self, call):
    add_pending_action(call, 'stake')


################        SABOTAGE        ################

@callback_execution.task(bind=True)
def exploit_opp_callback_task(self, call):
    if not check_if_cex_partner(call):
        add_pending_action(call, 'exploit_opp')
    else:
        bot.send_message(call['message']['chat']['id'], "❌ You are a CEX partner, you can't exploit opponents.")



@callback_execution.task(bind=True)
def fud_opp_callback_task(self, call):
    add_pending_action(call, 'fud_opp')


@callback_execution.task(bind=True)
def dox_opp_callback_task(self, call):
    add_pending_action(call, 'dox_opp')


@callback_execution.task(bind=True)
def flash_loan_callback_task(self, call):
    print('trying to dox')
    add_pending_action(call, 'flash_loan')


################        STRATEGY        ################

@callback_execution.task(bind=True)
def hire_shillers_callback_task(self, call):
    add_pending_action(call, 'hire_shillers')


@callback_execution.task(bind=True)
def cex_partnership_callback_task(self, call):
    add_pending_action(call, 'cex_partnership')


@callback_execution.task(bind=True)
def burn_tokens_callback_task(self, call):
    add_pending_action(call, 'burn_tokens')


@callback_execution.task(bind=True)
def action_four_callback_task(self, call):
    add_pending_action(call, 'four')


@callback_execution.task(bind=True)
def hire_hackers_callback_task(self, call):
    add_pending_action(call, 'hire_hackers')


@callback_execution.task(bind=True)
def kill_inversebrah_callback_task(self, call):
    add_pending_action(call, 'kill_inversebrah')



##################################          INFOS         #######################################


# Define the task to delete a message
@callback_execution.task(bind=True)
def delete_message_task(self, chat_id, message_id):
    bot.delete_message(chat_id, message_id)



######################### ABANDON ########################

@callback_execution.task(bind=True)
def abandon_game_task(self, chat_id):
    abandon_game_func(chat_id)




@callback_execution.task(bind=True)
def exit_matchmaking_task(self, call):
    chat_id = call['message']['chat']['id']

    lock = FileLock(f'{WAITING_PLAYERS_FILE}.lock')
    with lock:
        with open(WAITING_PLAYERS_FILE, 'r') as f:
            waiting_players = json.load(f)
        try:
            waiting_players.remove(str(chat_id))
        except:
            pass

        with open(WAITING_PLAYERS_FILE, 'w') as f:
            json.dump(waiting_players, f, indent=2)

    # confirmation to user
    bot.send_message(chat_id, "✅_You've been removed from the matchmaking system_", parse_mode='Markdown')

    return