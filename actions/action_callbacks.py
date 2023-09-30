
from actions.action_tasks import *



################        RESOURCE        ################

@bot.callback_query_handler(func=lambda call: call.data == 'raise_for_new_L2')
def raise_for_new_L2_callback(call):
    serialized_call = serialize_call(call)
    raise_for_new_L2_callback_task.apply_async(args=[serialized_call])



@bot.callback_query_handler(func=lambda call: call.data == 'farm_airdrop')
def farm_airdrop_callback(call):
    serialized_call = serialize_call(call)
    farm_airdrop_callback_task.apply_async(args=[serialized_call])


@bot.callback_query_handler(func=lambda call: call.data == 'deploy_memecoin')
def deploy_memecoin_callback(call):
    serialized_call = serialize_call(call)
    deploy_memecoin_callback_task.apply_async(args=[serialized_call])


@bot.callback_query_handler(func=lambda call: call.data == 'rug_pull')
def rug_pull_callback(call):
    serialized_call = serialize_call(call)
    rug_pull_callback_task.apply_async(args=[serialized_call])


@bot.callback_query_handler(func=lambda call: call.data == 'pump_and_dump')
def pump_and_dump_callback(call):
    serialized_call = serialize_call(call)
    pump_and_dump_callback_task.apply_async(args=[serialized_call])


@bot.callback_query_handler(func=lambda call: call.data == 'stake')
def stake_callback(call):
    serialized_call = serialize_call(call)
    stake_callback_task.apply_async(args=[serialized_call])


################        SABOTAGE        ################

@bot.callback_query_handler(func=lambda call: call.data == 'exploit_opp')
def exploit_opp_callback(call):
    serialized_call = serialize_call(call)
    exploit_opp_callback_task.apply_async(args=[serialized_call])


@bot.callback_query_handler(func=lambda call: call.data == 'fud_opp')
def fud_opp_callback(call):
    serialized_call = serialize_call(call)
    fud_opp_callback_task.apply_async(args=[serialized_call])


@bot.callback_query_handler(func=lambda call: call.data == 'dox_opp')
def dox_opp_callback(call):
    serialized_call = serialize_call(call)
    dox_opp_callback_task.apply_async(args=[serialized_call])


@bot.callback_query_handler(func=lambda call: call.data == 'flash_loan')
def flash_loan_callback(call):
    serialized_call = serialize_call(call)
    flash_loan_callback_task.apply_async(args=[serialized_call])


################        STRATEGY        ################

@bot.callback_query_handler(func=lambda call: call.data == 'hire_shillers')
def hire_shillers_callback(call):
    serialized_call = serialize_call(call)
    hire_shillers_callback_task.apply_async(args=[serialized_call])


@bot.callback_query_handler(func=lambda call: call.data == 'cex_partnership')
def cex_partnership_callback(call):
    serialized_call = serialize_call(call)
    cex_partnership_callback_task.apply_async(args=[serialized_call])


@bot.callback_query_handler(func=lambda call: call.data == 'burn_tokens')
def burn_tokens_callback(call):
    serialized_call = serialize_call(call)
    burn_tokens_callback_task.apply_async(args=[serialized_call])


@bot.callback_query_handler(func=lambda call: call.data == 'four')
def action_four_callback(call):
    serialized_call = serialize_call(call)
    action_four_callback_task.apply_async(args=[serialized_call])


@bot.callback_query_handler(func=lambda call: call.data == 'hire_hackers')
def hire_hackers_callback(call):
    serialized_call = serialize_call(call)
    hire_hackers_callback_task.apply_async(args=[serialized_call])


@bot.callback_query_handler(func=lambda call: call.data == 'kill_inversebrah')
def kill_inversebrah_callback(call):
    serialized_call = serialize_call(call)
    kill_inversebrah_callback_task.apply_async(args=[serialized_call])


##############################



@bot.callback_query_handler(func=lambda call: call.data == 'exit_matchmaking')
def exit_matchmaking(call):
    serialized_call = serialize_call(call)
    exit_matchmaking_task.apply_async(args=[serialized_call])