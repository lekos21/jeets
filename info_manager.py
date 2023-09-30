from config import *
from actions.action_tasks import delete_message_task

info_countdown = 20

# Handle the /zach_thread command
@bot.message_handler(commands=['zach_thread'])
def zach_thread_info(message):
    sent_message = bot.send_message(message.chat.id, f"*Zach Thread*: roll a dice with x% chances of Zach Thread. If successful, you lose 7-12🔥 and 7-12🟡.",
                                    parse_mode='Markdown')

    # Schedule the deletion
    delete_message_task.apply_async(args=[message.chat.id, message.message_id], countdown=info_countdown)  
    delete_message_task.apply_async(args=[message.chat.id, sent_message.message_id], countdown=info_countdown)  



# Handle the /FUD command
@bot.message_handler(commands=['fudded'])
def fudded_info_wrap(message):
    fud_info(message)

@bot.message_handler(commands=['fud'])
def fud_info_wrap(message):
    fud_info(message)

def fud_info(message):
    sent_message = bot.send_message(message.chat.id, f"*FUD*: 🟡 gains are reduced by x% (no effect on staking)",
                                    parse_mode='Markdown')

    # Schedule the deletion
    delete_message_task.apply_async(args=[message.chat.id, message.message_id], countdown=info_countdown)  
    delete_message_task.apply_async(args=[message.chat.id, sent_message.message_id], countdown=info_countdown)  
    
    

# Handle the /zach_thread command
@bot.message_handler(commands=['doxed'])
def doxed_info(message):
    sent_message = bot.send_message(message.chat.id, f"*Doxed*: you can't _Rug Pull_ or _Pump and Dump_.",
                                    parse_mode='Markdown')

    # Schedule the deletion
    delete_message_task.apply_async(args=[message.chat.id, message.message_id], countdown=info_countdown)  
    delete_message_task.apply_async(args=[message.chat.id, sent_message.message_id], countdown=info_countdown)  
    


# Handle the /zach_thread command
@bot.message_handler(commands=['CEX'])
def doxed_info(message):
    sent_message = bot.send_message(message.chat.id, f"*CEX Partnership*: +35%🟡 on _Raise_ and _Memecoin deployment_ for the "
                                                     f"rest of the game, but you can't _Rug Pull_ or _Exploit_.",
                                    parse_mode='Markdown')

    # Schedule the deletion
    delete_message_task.apply_async(args=[message.chat.id, message.message_id], countdown=info_countdown)  
    delete_message_task.apply_async(args=[message.chat.id, sent_message.message_id], countdown=info_countdown)