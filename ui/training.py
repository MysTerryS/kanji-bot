from telebot import types
from os import getcwd
from random import choice, shuffle

from bot_instance import bot
from constants import *
from ui.state import user_state

from database import SelectKanjiCount
from services.info import InfoAboutKanji
from services.image import create_kanji_image
from services.randomizer import SelectRandomKanji

from ui.client import ShowDisplayClientMode
from database import UpdateKanjiForUser, select_kanji

from models import Kanji

def ShowTrainerDisplay(message, mode):
    user_state[message.chat.id]["mode"] = mode
    user_state[message.chat.id]["state"] = "trainer"
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard = True)
    keyboard.add(types.KeyboardButton(text = KANJI_TO_ONYOMI_KEY))
    keyboard.add(types.KeyboardButton(text = ONYOMI_TO_KANJI_KEY))
    keyboard.add(types.KeyboardButton(text = KANJI_TO_KUNYOMI_KEY))
    keyboard.add(types.KeyboardButton(text = KUNYOMI_TO_KANJI_KEY))
    keyboard.add(types.KeyboardButton(text = KANJI_TO_ENG_KEY))
    keyboard.add(types.KeyboardButton(text = ENG_TO_KANJI_KEY))
    keyboard.add(types.KeyboardButton(text = KANJI_TO_RUS_KEY))
    keyboard.add(types.KeyboardButton(text = RUS_TO_KANJI_KEY))
    keyboard.add(types.KeyboardButton(text = CANCEL_KEY))
    bot.send_message(message.chat.id,
                     "Which quiz do you want?",
                     reply_markup = keyboard)
    
def SelectMode(message, mode, isKanji = True):
    chat_id = message.chat.id
    kanjiCount = SelectKanjiCount(chat_id)
    if kanjiCount < 4:
        bot.send_message(
            chat_id,
            text = "❌ You must be have at least 4 kanjies in your learning list."
        )
        return
    user_state[chat_id]["correct"] = 0
    user_state[chat_id]["wrong"] = 0
    if isKanji:
        if user_state[chat_id]["mode"] == "quiz":
            KanjiQuizDisplay(message, mode)
        else:
            KanjiTypingDisplay(message, mode)
    else:
        if user_state[message.chat.id]["mode"] == "quiz":
            MeanReadQuizDisplay(message, mode)
        else:
            MeanReadTypingDisplay(message, mode)

def KanjiQuizDisplayNextStep(message, mode, isTyping = False, isMode = False):
    chat_id = message.chat.id
    if message.text == FINISH_KEY:
        bot.send_message(chat_id,
                         text = "🏁You'd finished. Your result:\n✅Correct: {}\n❌Wrong: {}\n\n📈Accuracy: {}%".format(
                             user_state[chat_id]["correct"],
                             user_state[chat_id]["wrong"],
                             round((user_state[chat_id]["correct"] / (user_state[chat_id]["correct"] + user_state[chat_id]["wrong"])), 2) * 100
                         ))
        user_state[chat_id].pop("correct")
        user_state[chat_id].pop("wrong")
        ShowDisplayClientMode(message)
        return
    kanji = Kanji()
    kanji.hieroglyph = user_state[chat_id]["kanji"]
    kanji_id = select_kanji(kanji)
    if not isTyping and message.text == user_state[chat_id]["in"] or isTyping and message.text in user_state[chat_id]["in"]:
        user_state[chat_id]["correct"] += 1
        UpdateKanjiForUser(chat_id, kanji_id, True)
        answer = "✅Correct" 
    else:
        user_state[chat_id]["wrong"] += 1
        UpdateKanjiForUser(chat_id, kanji_id, False)
        answer = "❌Wrong\nYour answer: {}\nCorrect: {}".format(message.text, user_state[chat_id]["in"])
        answer += InfoAboutKanji(user_state[chat_id]["kanji"], True)
    bot.send_message(
        chat_id,
        text = answer
    )
    if not isMode:
        if not isTyping:
            KanjiQuizDisplay(message, mode)
        else:
            KanjiTypingDisplay(message, mode)
    else:
        if not isTyping:
            MeanReadQuizDisplay(message, mode)
        else:
            MeanReadTypingDisplay(message, mode)

def KanjiQuizDisplay(message, mode):
    chat_id = message.chat.id
    modes = dict()
    kanjiList, modes = SelectRandomKanji(mode, chat_id, 0)
    mainKanji = choice(kanjiList)
    user_state[chat_id]["in"] = modes[mainKanji]
    user_state[chat_id]["kanji"] = mainKanji
    modes = list(modes.values())
    shuffle(modes)
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard = True)
    for value in modes:
        keyboard.add(types.KeyboardButton(text = value))
    keyboard.add(types.KeyboardButton(text = FINISH_KEY))
    path_to_kanji = getcwd() + "{}.png".format(mainKanji)
    create_kanji_image(mainKanji, path_to_kanji)
    msg = bot.send_message(chat_id,
                    text = "Choose correct answer",
                    reply_markup = keyboard)
    with open(path_to_kanji, "rb") as file:
        bot.send_photo(
            message.chat.id,
            file
        )
    bot.register_next_step_handler(msg, KanjiQuizDisplayNextStep, mode)

def MeanReadQuizDisplay(message, mode):
    chat_id = message.chat.id
    kanjiList, modes = SelectRandomKanji(mode, chat_id, 0)
    mainKanji = choice(kanjiList)
    user_state[chat_id]["in"] = mainKanji
    user_state[chat_id]["kanji"] = mainKanji
    shuffle(kanjiList)
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard = True)
    for kanji in kanjiList:
        keyboard.add(types.KeyboardButton(text = kanji))
    keyboard.add(types.KeyboardButton(text = FINISH_KEY))
    msg = bot.send_message(chat_id,
                           text = "{}".format(modes[mainKanji]),
                           reply_markup = keyboard)
    bot.register_next_step_handler(msg, KanjiQuizDisplayNextStep, mode, False, True)

def KanjiTypingDisplay(message, mode):
    chat_id = message.chat.id
    kanji, value = SelectRandomKanji(mode, chat_id, 0, True)
    user_state[chat_id]["in"] = value
    user_state[chat_id]["kanji"] = kanji
    TypingTemplate(chat_id, kanji, mode)

def MeanReadTypingDisplay(message, mode):
    chat_id = message.chat.id
    kanji, value = SelectRandomKanji(mode, chat_id, 0, True)
    value = choice(value)
    user_state[chat_id]["in"] = kanji
    user_state[chat_id]["kanji"] = kanji
    TypingTemplate(chat_id, value, mode, True)

def MeanReadTypingDisplay(message, mode):
    chat_id = message.chat.id
    kanji, value = SelectRandomKanji(mode, chat_id, 0, True)
    value = choice(value)
    user_state[chat_id]["in"] = kanji
    user_state[chat_id]["kanji"] = kanji
    TypingTemplate(chat_id, value, mode, True)

def TypingTemplate(chat_id, value, mode, isMode = False):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard = True)
    keyboard.add(types.KeyboardButton(text = FINISH_KEY))
    msg = bot.send_message(
        chat_id,
        text = "Enter {}".format(mode) if not isMode else "{}".format(value),
        reply_markup = keyboard)
    if not isMode:
        path_to_text = getcwd() + "{}.png".format(value)
        create_kanji_image(value, path_to_text)
        with open(path_to_text, "rb") as file:
            bot.send_photo(
                chat_id,
                file
            )
    bot.register_next_step_handler(msg, KanjiQuizDisplayNextStep, mode, True, isMode)