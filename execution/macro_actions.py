from config import *


def new_turn(game_data):
    chat_id1 = game_data['player1']['chat_id']
    chat_id2 = game_data['player2']['chat_id']
    send_action_categories(chat_id1)
    send_action_categories(chat_id2)

def send_action_categories(chat_id):
    markup = InlineKeyboardMarkup()
    markup.row_width = 3
    resource_button = InlineKeyboardButton("🟢 Resource", callback_data=f"resource")
    sabotage_button = InlineKeyboardButton("🔴 Sabotage", callback_data=f"sabotage")
    strategic_button = InlineKeyboardButton("🔵 Strategy", callback_data=f"strategic")
    markup.add(resource_button, sabotage_button, strategic_button)

    bot.send_message(chat_id, "*Resource*: _gather and protect your gold_\n"
                              "*Sabotage*: _damage the opponent and steal from him_\n"
                              "*Strategy*: _grow your stats and gain bonus_", reply_markup=markup, parse_mode='Markdown')


@bot.callback_query_handler(func=lambda call: call.data.startswith('resource'))
def send_resource_actions(call):
    turn = call.data.split("_")[-1]
    chat_id = call.message.chat.id

    # delete macro button
    bot.delete_message(chat_id, call.message.message_id)

    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(
        InlineKeyboardButton("Raise Funds", callback_data=f"raise_for_new_L2"),
        InlineKeyboardButton("Farm Airdrop", callback_data=f"farm_airdrop"),
        InlineKeyboardButton("Deploy Memecoin", callback_data=f"deploy_memecoin"),
        InlineKeyboardButton("Rug pull", callback_data=f"rug_pull"),
        InlineKeyboardButton("Pump and Dump", callback_data=f"pump_and_dump"),
        InlineKeyboardButton("Stake", callback_data=f"stake"),
        InlineKeyboardButton("❌ Go back", callback_data=f"go_back_to_macro")
    )

    msg = '''
• <b>Raise Funds</b>: gain +3🔥 and +15🟡. Roll to gain additional 12-24🟡 (chances 0-60% based on 🔥 diff. up, max at +24)
• <b>Farm airdrop</b>: gain 9-24🟡 and 3-6💊
• <b>Deploy Memecoin</b>: put 70% of your 🟡 in an LP, randomly get back 80-110% on the LP you provide (add 0.33% to the roll for each 🔥 point)
• <b>Rug Pull</b>: gain 15🟡 and 6💊. gain 0-16🟡 based on 💊 diff. up to +24. 20% chances of /zach_thread
• <b>PnD</b>: gain 12-36🟡 based on 🔥 diff. (max at +24). 20% chances of /zach_thread
• <b>Stake</b>: stake 40% of your 🟡 for the rest of the turn, then get it back with 25% yield. Staked coins can't be stolen!
'''

    bot.send_message(chat_id, f"{msg}", reply_markup=markup, parse_mode='HTML')

    return



@bot.callback_query_handler(func=lambda call: call.data.startswith('sabotage'))
def send_sabotage_actions(call):
    turn = call.data.split("_")[-1]
    chat_id = call.message.chat.id

    # delete macro button
    bot.delete_message(chat_id, call.message.message_id)

    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    # Add buttons for each resource action here
    markup.add(
        InlineKeyboardButton("Exploit", callback_data=f"exploit_opp"),
        InlineKeyboardButton("FUD", callback_data=f"fud_opp"),
        InlineKeyboardButton("Dox", callback_data=f"dox_opp"),
        InlineKeyboardButton("Flash Loan", callback_data=f"flash_loan"),
        InlineKeyboardButton("❌ Go back", callback_data=f"go_back_to_macro"),
    )

    msg = '''
• *Exploit*: roll to steal 25% of opponent 🟡 and reduce his 🔥 by 3-9 (chances 19%-99% based on 💊 diff, max at +36)
• *FUD*: reduce by 20-50% 🟡 gathered by the opponent for the next turn and make him lose 6-24 🟡 (both based on 🔥 diff, max at 24. No effect on staking). Then lose 9 🔥. _(FUD has no effect on Staking gains)_.
• *Dox*: opp lose 6 🔥. Roll to dox him (chances 33%-99% based on 💊 diff, max at +24). A doxed player can't Rug Pull and PnD for the rest of the game (starting from the next turn).
• *Flash Loan*: gain 25 🟡. If you have less gold than your opponent, steal 20 🟡 from him. pay 26 🟡.
    '''

    bot.send_message(chat_id, f"{msg}", reply_markup=markup, parse_mode='Markdown')


@bot.callback_query_handler(func=lambda call: call.data.startswith('strategic'))
def send_strategic_actions(call):
    turn = call.data.split("_")[-1]
    chat_id = call.message.chat.id

    # delete macro button
    bot.delete_message(chat_id, call.message.message_id)

    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    # Add buttons for each resource action here
    markup.add(
        InlineKeyboardButton("Hire Shillers", callback_data=f"hire_shillers"),
        InlineKeyboardButton("Cex partnership", callback_data=f"cex_partnership"),
        InlineKeyboardButton("Burn tokens", callback_data=f"burn_tokens"),
        InlineKeyboardButton("4", callback_data=f"four"),
        InlineKeyboardButton("Hire hackers", callback_data=f"hire_hackers"),
        InlineKeyboardButton("Kill Inversebrah", callback_data=f"kill_inversebrah"),
        InlineKeyboardButton("❌ Go back", callback_data=f"go_back_to_macro"),
    )

    msg = '''
• *Hire shillers*: pay 12-18🟡 to gain +15🔥. remove any FUD effect. 
• *CEX partnership*: pay 20🟡 to gain 6🔥 and 6💊. you get 35% more 🟡 if you raise or deploy memecoins for the rest of the game. You can't Rugpull or Exploit for the rest of the game.
• *Burn tokens*: pay 15🟡 to gain 25-40🔥 for the next turn 
• *4*: Pay 4🟡. you are immune from exploits for this turn. Roll 4 times with 44% chance of success. for each success, -4🟡, +4🔥 and +4💊. 
• *Hire hackers*: pay 15🟡 to gain 10💊. if you have less autism than the opponent, gain 8-15💊.
• *Kill inversebrah*: gain 8🟡 and 6💊. if the opponent have more 🟡 and 🔥 than you, steal 8 🔥 from him 
        '''

    bot.send_message(chat_id, f"{msg}", reply_markup=markup, parse_mode='Markdown')



@bot.callback_query_handler(func=lambda call: call.data == 'go_back_to_macro')
def delete_message(call):
    chat_id = call.message.chat.id
    message_id = call.message.message_id
    bot.delete_message(chat_id, message_id)
    send_action_categories(chat_id)