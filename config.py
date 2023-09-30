import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from filelock import FileLock
import json
import os
import time
import logging
import random
import copy
from dotenv import load_dotenv
load_dotenv()

etherscan_api = os.getenv('ETHERSCAN_API')
BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
bot = telebot.TeleBot(BOT_TOKEN)
WAITING_PLAYERS_FILE = 'games_data/waiting_players.json'
current_games_lock = FileLock('current_games.json.lock')

logging.basicConfig(filename='activity.log', level=logging.DEBUG,
                    format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')


# in minutes
turn_duration = 10
