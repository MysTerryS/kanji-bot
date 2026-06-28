from telebot import types

from bot_instance import bot
from constants import *
from ui.state import user_state

from settings import set_default, get_user_settings, ShowSettings

# Displays
def ShowModeDisplay(message):
    chat_id = message.chat.id
    set_default(chat_id)
    user_state[chat_id] = dict()
    user_state[chat_id]["state"] = 0
    user_state[chat_id]["level"] = get_user_settings(chat_id)["radical_level"]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard = True)
    keyboard.add(types.KeyboardButton(text = DEV_KEY))
    keyboard.add(types.KeyboardButton(text = CLI_KEY))
    keyboard.add(types.KeyboardButton(text = SETTINGS_KEY))
    bot.send_message(message.chat.id,
                     "Choose a mode",
                     reply_markup = keyboard)
    
def ShowDeveloperMode(message):
    user_state[message.chat.id]["state"] = 1
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard = True)
    keyboard.add(types.KeyboardButton(text = ADD_KANJI_KEY))
    keyboard.add(types.KeyboardButton(text = ADD_RADICAL_KEY))
    keyboard.add(types.KeyboardButton(text = ADD_WORD_KEY))
    keyboard.add(types.KeyboardButton(text = SHOW_KANJI_KEY))
    keyboard.add(types.KeyboardButton(text = SHOW_ALL_KANJI_KEY))
    keyboard.add(types.KeyboardButton(text = IMPORT_EXCEL_KEY))
    keyboard.add(types.KeyboardButton(text = IMPORT_TXT_KEY))
    keyboard.add(types.KeyboardButton(text = EXPORT_EXCEL_KEY))
    keyboard.add(types.KeyboardButton(text = EXPORT_TXT_KEY))
    keyboard.add(types.KeyboardButton(text = LOAD_RADICAL_TABLE_EXCEL_KEY))
    keyboard.add(types.KeyboardButton(text = LOAD_RADICAL_TABLE_TXT_KEY))
    keyboard.add(types.KeyboardButton(text = LINK_KANJI_TO_RADICAL_KEY))
    keyboard.add(types.KeyboardButton(text = EXPORT_KANJI_RADICALS_KEY))
    keyboard.add(types.KeyboardButton(text = LOAD_LINKS_TABLE_KEY))
    keyboard.add(types.KeyboardButton(text = CANCEL_KEY))
    #keyboard.add(types.KeyboardButton(text = SHARE_KANJI_TO_RADICALS_KEY))
    bot.send_message(message.chat.id,
                     "Select your next doing",
                     reply_markup = keyboard)
    
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
    
def BackToPrevious(message):
    state = user_state[message.chat.id]["state"]
    if state == 1:
        ShowModeDisplay(message)
    elif state == "setLevel":
        ShowSettings(message)
    elif state in ["trainer", "learning"]:
        ShowDisplayClientMode(message)