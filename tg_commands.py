from config import *
from new_game import new_game_request
from actions.action_tasks import abandon_game_task

@bot.message_handler(commands=['start'])
def send_welcome(message):
    chat_id = message.chat.id
    lock1 = FileLock('users_data/user_sample.json.lock')

    # Load the user_sample
    with lock1:
        with open('users_data/user_sample.json', 'r') as f:
            user_sample = json.load(f)

    user_sample['chat_id'] = chat_id

    # Create the new user
    lock2 = FileLock(f'users_data/id_{chat_id}.json.lock')
    with lock2:
        with open(f'users_data/id_{chat_id}.json', 'w') as f:
            json.dump(user_sample, f, indent=2)

    bot.reply_to(message, f"Welcome to Jeeters, the CT PVP game on Telegram. \n"
                          f"- Each round, both players select 2 actions that will be executed in alternate order.\n"
                          f"- The game ends after 6 rounds.\n"
                          f"- Who gets more gold at the end of the game.\n\n"
                          f"Please choose a username:")
    # Set user state to awaiting username
    set_user_state(chat_id, 'AWAITING_USERNAME')


@bot.message_handler(func=lambda message: get_user_state(message.chat.id) == 'AWAITING_USERNAME')
def set_username(message):
    chat_id = message.chat.id
    set_user_state(chat_id, '')
    username = str(message.text.split()[0][:23])
    lock = FileLock(f'users_data/id_{chat_id}.json.lock')

    with lock:
        with open(f'users_data/id_{chat_id}.json', 'r') as f:
            user_data = json.load(f)

        user_data['label'] = username

        with open(f'users_data/id_{chat_id}.json', 'w') as f:
            json.dump(user_data, f, indent=2)


    bot.send_message(chat_id, f"Welcome {username}, press /new_game to enter the matchmaking",
                     parse_mode='HTML')
    return


@bot.message_handler(commands=['new_game'])
def new_game_command(message):
    new_game_request(str(message.chat.id))
    return



@bot.message_handler(commands=['abandon_game'])
def abandon_game_wrapper(message):
    chat_id = message.chat.id
    abandon_game_task.apply_async(args=[chat_id])
    return





@bot.message_handler(commands=['personal_stats'])
def personal_stats(message):
    chat_id = message.chat.id

    lock = FileLock(f'users_data/id_{chat_id}.json.lock')
    with lock:
        with open(f'users_data/id_{chat_id}.json', 'r') as f:
            user_sample = json.load(f)

    wins = user_sample["win"] + user_sample["win_by_abandon"]
    losses = user_sample["loss"] + user_sample["loss"]
    streak = user_sample["streak"]
    badges = "_(Coming soon)_"

    msg = (f"*SEASON 1*\n\n"
           f"*Wins*: {wins}\n"
           f"*Losses*: {losses}\n"
           f"*Current Streak*: {streak}\n"
           f"*Badges*: {badges}")

    bot.send_message(chat_id, msg, parse_mode='Markdown')

    return





def get_user_state(chat_id):
    lock = FileLock(f'users_data/id_{chat_id}.json.lock')
    with lock:
        with open(f'users_data/id_{chat_id}.json', 'r') as f:
            data = json.load(f)
        return data.get('user_state')


def set_user_state(chat_id, state):
    lock = FileLock(f'users_data/id_{chat_id}.json.lock')
    with lock:
        with open(f'users_data/id_{chat_id}.json', 'r') as f:
            user_data = json.load(f)

        user_data['user_state'] = state

        with open(f'users_data/id_{chat_id}.json', 'w') as f:
            json.dump(user_data, f, indent=2)



############### Command descriptions abt specific topics #################

@bot.message_handler(commands=['FUD'])
def personal_stats(message):
    pass