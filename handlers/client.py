from bot_instance import bot
from constants import *
from ui.training import (
    ShowTrainerDisplay,
    SelectMode
)
from ui.learning import (
    ShowLearningDisplay,
    LearnByRadicalDisplay,
    SearchByOnyomiDisplay,
    SearchByKunyomiDisplay
)

@bot.message_handler(func = lambda message: message.text == QUIZ_KEY)
def Quiz(message):
    ShowTrainerDisplay(message, "quiz")

@bot.message_handler(func = lambda message: message.text == TYPING_KEY)
def Typing(message):
    ShowTrainerDisplay(message, "typing")

@bot.message_handler(func = lambda message: message.text == KANJI_TO_ONYOMI_KEY)
def KanjiQuizOnyomi(message):
    SelectMode(message, "onyomi")

@bot.message_handler(func = lambda message: message.text == ONYOMI_TO_KANJI_KEY)
def OnyomiQuizKanji(message):
    SelectMode(message, "onyomi", False)

@bot.message_handler(func = lambda message: message.text == KANJI_TO_KUNYOMI_KEY)
def KanjiQuizKuniomi(message):
    SelectMode(message, "kunyomi")

@bot.message_handler(func = lambda message: message.text == KUNYOMI_TO_KANJI_KEY)
def KunyomiQuiz(message):
    SelectMode(message, "kunyomi", False)

@bot.message_handler(func = lambda message: message.text == KANJI_TO_ENG_KEY)
def KanjiQuizEng(message):
    SelectMode(message, "eng")

@bot.message_handler(func = lambda message: message.text == ENG_TO_KANJI_KEY)
def EngQuizKanji(message):
    SelectMode(message, "eng", False)

@bot.message_handler(func = lambda message: message.text == KANJI_TO_RUS_KEY)
def KanjiQuizRus(message):
    SelectMode(message, "rus")

@bot.message_handler(func = lambda message: message.text == RUS_TO_KANJI_KEY)
def RusQuizKanji(message):
    SelectMode(message, "rus", False)

@bot.message_handler(func = lambda message: message.text == LEARN_NEW_KEY)
def LearnNew(message):
    ShowLearningDisplay(message)

@bot.message_handler(func = lambda message: message.text == LEARN_BY_RADICAL_NEW_KEY)
def LearnByRadical(message):
    LearnByRadicalDisplay(message)

@bot.message_handler(func = lambda message: message.text == SEARCH_BY_ONYOMI_KEY)
def SearchByOnyomi(message):
    SearchByOnyomiDisplay(message)

@bot.message_handler(func = lambda message: message.text == SEARCH_BY_KUNYOMI_KEY)
def SearchByKunyomi(message):
    SearchByKunyomiDisplay(message)