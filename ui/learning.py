from telebot import types
from os import getcwd

from bot_instance import bot
from constants import *
from ui.state import user_state

from users import (
    CheckUser,
    UserToRadical,
    SelectLearnRadical,
    SelectLearnKanji
)

from database import (
    select_radical,
    SetStatusRadical,
    DeleteRadicalFromUser,
    SelectKanjiForUser
)

from services.image import create_kanji_image
from services.info import InfoAboutKanji
from services.search import MakeKanjiFromOnyomi, MakeKanjiFromKunyomi, GetKanjiID

from ui.client import ShowDisplayClientMode

def ShowLearningDisplay(message):
    user_state[message.chat.id]["state"] = "learning"
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard = True)
    keyboard.add(types.KeyboardButton(text = LEARN_BY_RADICAL_NEW_KEY))
    keyboard.add(types.KeyboardButton(text =  SEARCH_BY_ONYOMI_KEY))
    keyboard.add(types.KeyboardButton(text = SEARCH_BY_KUNYOMI_KEY))
    keyboard.add(types.KeyboardButton(text = CANCEL_KEY))
    bot.send_message(message.chat.id,
                     "Select mode of studying",
                     reply_markup = keyboard)
    
def LearnByRadicalDisplay(message):
    user = CheckUser(message.chat.id)
    user_state[message.chat.id]["state"] = "by_radical"
    radicals = UserToRadical(
        message.chat.id, 
        0, 
        user_state[message.chat.id]["level"])
    user_state[message.chat.id]["radicals"] = radicals
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard = True)
    for radical in radicals:
        keyboard.add(types.KeyboardButton(text = radical))
    keyboard.add(types.KeyboardButton(text = CANCEL_KEY))
    keyboard.add(types.KeyboardButton(text = UPDATE_KEY))
    msg = bot.send_message(
        message.chat.id,
        text = "You've available the next radicals for study. Choose one.",
        reply_markup = keyboard
    )
    bot.register_next_step_handler(msg, RadicalHasSelected)

def RadicalHasSelected(message, isKanjiNext = False):
    if message.text == CANCEL_KEY:
        ShowLearningDisplay(message)
        return
    elif message.text == UPDATE_KEY:
        UpdateRadicals(message, user_state[message.chat.id]["radicals"])
        return
    if not isKanjiNext:
        kanjiList = SelectLearnRadical(message.chat.id, message.text)
        user_state[message.chat.id]["kanjiList"] = kanjiList
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard = True)
    for kanji in user_state[message.chat.id]["kanjiList"]:
        keyboard.add(types.KeyboardButton(text = kanji))
    keyboard.add(CONTINUE_KEY)
    msg = bot.send_message(
        message.chat.id,
        text = "You've available the next kanjies for study. Select which you want to learn." if not isKanjiNext else "Next...",
        reply_markup = keyboard
    )
    bot.register_next_step_handler(msg, KanjiHasSelected)

def KanjiHasSelected(message):
    if message.text == CONTINUE_KEY:
        bot.send_message(
            message.chat.id,
            text = "I've saved your kanji.\nYou can learning it in the quiz or typing.\nGood luck"
        )
        ShowDisplayClientMode(message)
    else:
        SelectLearnKanji(message.chat.id, message.text)
        if message.text in user_state[message.chat.id]["radicals"]:
            radical_id = select_radical(message.text)
            SetStatusRadical(message.chat.id, radical_id, 1)
        user_state[message.chat.id]["kanjiList"].remove(message.text)
        RadicalHasSelected(message, True)

def UpdateRadicals(message, radicals):
    for radical in radicals:
        radical_id = select_radical(radical)
        DeleteRadicalFromUser(message.chat.id, radical_id)
    LearnByRadicalDisplay(message)

def SearchingProcess(message):
    if not "kanjies" in user_state[message.chat.id]:
        if user_state[message.chat.id]["search_by"] == "onyomi":
            kanjies = MakeKanjiFromOnyomi(message.text)
        else:
            kanjies = MakeKanjiFromKunyomi(message.text)
    else:
        kanjies = user_state[message.chat.id]["kanjies"]
    if kanjies:
        user_state[message.chat.id]["kanjies"] = kanjies
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard = True)
        for kanji in kanjies:
            keyboard.add(types.KeyboardButton(text = kanji))
        keyboard.add(types.KeyboardButton(text = CANCEL_KEY))
        msg = bot.send_message(
            message.chat.id,
            text = "Here is your result" 
                if "kanjies" in user_state[message.chat.id]
                else "We've back again",
            reply_markup = keyboard
        )
        bot.register_next_step_handler(msg, KanjiWasSelected)
    else:
        bot.send_message(
            message.chat.id,
            text = "Nothing at all"
        )

def KanjiWasSelected(message):
    if message.text == CANCEL_KEY:
        ShowDisplayClientMode(message)
        return
    user_state[message.chat.id]["kanji"] = message.text
    path_to_kanji = getcwd() + "{}.png".format(message.text)
    create_kanji_image(message.text, path_to_kanji)
    infoAboutKanji = InfoAboutKanji(message.text)
    allKanjies = SelectKanjiForUser(message.chat.id, 0)
    kanjiInAllKanjies = (GetKanjiID(message.text), ) in allKanjies
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard = True)
    keyboard.add(types.KeyboardButton(text = YES_KEY))
    keyboard.add(types.KeyboardButton(text = NO_KEY))
    keyboardAlternive = types.ReplyKeyboardMarkup(resize_keyboard = True)
    keyboardAlternive.add(types.KeyboardButton(text = CONTINUE_KEY))
    with open(path_to_kanji, mode = "rb") as file:
        bot.send_photo(
            message.chat.id,
            file
        )
    msg = bot.send_message(
        message.chat.id,
        text = infoAboutKanji + "\n" + "Do you want to save it?" if not kanjiInAllKanjies else "Your kanji",
        reply_markup = keyboard if not kanjiInAllKanjies else keyboardAlternive
    )
    bot.register_next_step_handler(msg, SaveAfterSearchingOrNot)

def SaveAfterSearchingOrNot(message):
    if message.text == YES_KEY:
        SelectLearnKanji(
            message.chat.id, 
            user_state[message.chat.id]["kanji"]
        )
        bot.send_message(
            message.chat.id,
            text = "I've saved your kanji"
        )
        ShowDisplayClientMode(message)
    else:
        SearchingProcess(message)

def SearchByOnyomiDisplay(message):
    user_state[message.chat.id]["search_by"] = "onyomi"
    msg = bot.send_message(
        message.chat.id,
        text = "Send me text by katakana and I'll find for you similar kanji."
    )
    bot.register_next_step_handler(msg, SearchingProcess)

def SearchByKunyomiDisplay(message):
    user_state[message.chat.id]["search_by"] = "kunyomi"
    msg = bot.send_message(
        message.chat.id,
        text = "Send me text by hiragana and I'll find for you similar kanji."
    )
    bot.register_next_step_handler(msg, SearchingProcess)