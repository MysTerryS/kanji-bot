from bot_instance import bot
from constants import *
from ui.developer import (
    ShowAddKanjiDisplay,
    LinkKanjiToRadicalDisplay,
    ShowKanjiDisplay,
    ImportExcelDisplay,
    ImportTxtDisplay,
    ExportExcelDisplay,
    ExportTXTDisplay,
    LoadRadicalTable,
    ImportLinksTableDisplay,
    ShowAddWordDisplay
)
@bot.message_handler(func = lambda message: message.text == ADD_KANJI_KEY)
def AddKanjiInTelegram(message):
    ShowAddKanjiDisplay(message)

@bot.message_handler(func = lambda message: message.text == ADD_RADICAL_KEY)
def AddRadicalInTelegram(message):
    ShowAddKanjiDisplay(message, True)

@bot.message_handler(func = lambda message: message.text == LINK_KANJI_TO_RADICAL_KEY)
def LinkKanjiToRadicalInTelegram(message):
    LinkKanjiToRadicalDisplay(message)

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

@bot.message_handler(func = lambda message: message.text == EXPORT_KANJI_RADICALS_KEY)
def ExportRadicalsKanji(message):
    LoadRadicalTable(message)

@bot.message_handler(func = lambda message: message.text == LOAD_LINKS_TABLE_KEY)
def ImportLinksTable(message):
    ImportLinksTableDisplay(message)

@bot.message_handler(func = lambda message: message.text == ADD_WORD_KEY)
def AddWord(message):
    ShowAddWordDisplay(message)