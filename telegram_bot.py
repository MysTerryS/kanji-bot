from constants import *
from telegram_ui import *
from bot_instance import bot

# Telegram
@bot.message_handler(commands = ["start"])
def StartMessaging(message):
    ShowModeDisplay(message)

# Developer
@bot.message_handler(func = lambda message: message.text == DEV_KEY)
def Developer(message):
    ShowDeveloperMode(message)

@bot.message_handler(func = lambda message: message.text == ADD_KANJI_KEY)
def AddKanjiInTelegram(message):
    ShowAddKanjiDisplay(message)

@bot.message_handler(func = lambda message: message.text == ADD_RADICAL_KEY)
def AddRadicalInTelegram(message):
    ShowAddKanjiDisplay(message, True)

@bot.message_handler(func = lambda message: message.text == LINK_KANJI_TO_RADICAL_KEY)
def LinkKanjiToRadicalInTelegram(message):
    LinkKanjiToRadicalDisplay(message)

# I'll delete it, maybe
@bot.message_handler(func = lambda message: message.text == SHOW_ALL_KANJI_KEY)
def ShowAllKanjiInTelegram(message):
    ShowAllKanjiDisplay(message)

@bot.message_handler(func = lambda message: message.text == SHOW_KANJI_KEY)
def ShowKanji(message):
    ShowKanjiDisplay(message)

@bot.message_handler(func = lambda message: message.text == IMPORT_EXCEL_KEY)
def ImportExcel(message):
    ImportExcelDisplay(message)

@bot.message_handler(func = lambda message: message.text == IMPORT_TXT_KEY)
def ImportTXT(message):
    ImportTxtDisplay(message)

@bot.message_handler(func = lambda message: message.text == LOAD_RADICAL_TABLE_EXCEL_KEY)
def LoadRadicalsExcel(message):
    ImportExcelDisplay(message, True)

@bot.message_handler(func = lambda message: message.text == LOAD_RADICAL_TABLE_TXT_KEY)
def LoadRadicalsTXT(message):
    ImportTxtDisplay(message, True)

@bot.message_handler(func = lambda message: message.text == EXPORT_EXCEL_KEY)
def ExportExcel(message):
    ExportExcelDisplay(message)

@bot.message_handler(func = lambda message: message.text == EXPORT_TXT_KEY)
def ExportTXT(message):
    ExportTXTDisplay(message)

# Client
@bot.message_handler(func = lambda message: message.text == CLI_KEY)
def ClientMode(message):
    ShowDisplayClientMode(message)

@bot.message_handler(func = lambda message: message.text == QUIZ_KEY)
def Quiz(message):
    ShowQuizDisplay(message)

bot.polling(none_stop = True, interval = 0)