from telebot import types
from constants import *
from ui.state import user_state
from bot_instance import bot

def ShowDisplayClientMode(message):
    user_state[message.chat.id]["state"] = 1
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard = True)
    keyboard.add(types.KeyboardButton(text = QUIZ_KEY))
    keyboard.add(types.KeyboardButton(text = TYPING_KEY))
    keyboard.add(types.KeyboardButton(text = LEARN_NEW_KEY))
    keyboard.add(types.KeyboardButton(text = RECORDS_KEY))
    keyboard.add(types.KeyboardButton(text = STATS_KEY))
    keyboard.add(types.KeyboardButton(text = CANCEL_KEY))
    bot.send_message(message.chat.id,
                    "Select your next doing, please",
                    reply_markup = keyboard)