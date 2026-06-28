from telebot import types

from bot_instance import bot
from constants import *
from ui.state import user_state

from settings import (
    ShowSettings,
    update_radical_level
)

def SettingsDisplay(message):
    chat_id = message.chat.id
    user_state[chat_id]["state"] = 1
    answer = ShowSettings(chat_id)
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard = True)
    keyboard.add(types.KeyboardButton(text = LEVEL_KEY))
    keyboard.add(types.KeyboardButton(text = CANCEL_KEY))
    bot.send_message(
        chat_id,
        text = answer,
        reply_markup = keyboard
    )

def ShowSetLevelDisplay(message):
    user_state[message.chat.id]["state"] = "setLevel"
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard = True)
    for level in LEVELS.keys():
        keyboard.add(types.KeyboardButton(text = level))
    keyboard.add(types.KeyboardButton(text = CANCEL_KEY))
    msg = bot.send_message(
        message.chat.id,
        text = "Set your level",
        reply_markup = keyboard
    )
    bot.register_next_step_handler(message, LevelSetting)

def LevelSetting(message):
    if message.text == CANCEL_KEY:
        return
    update_radical_level(message.chat.id, LEVELS[message.text])
    SettingsDisplay(message)