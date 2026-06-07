from telebot import types
from constants import *
from utils import *
from bot_instance import bot
from excel import read_excel, put_kanji_in_excel
from txt import read_txt, put_kanji_in_txt
from os import getcwd

# States
user_state = {}

# Displays
def ShowModeDisplay(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard = True)
    keyboard.add(types.KeyboardButton(text = DEV_KEY))
    keyboard.add(types.KeyboardButton(text = CLI_KEY))
    bot.send_message(message.chat.id,
                     "Choose a mode",
                     reply_markup = keyboard)

# Developer
def ShowDeveloperMode(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard = True)
    keyboard.add(types.KeyboardButton(text = ADD_KANJI_KEY))
    keyboard.add(types.KeyboardButton(text = ADD_RADICAL_KEY))
    keyboard.add(types.KeyboardButton(text = SHOW_KANJI_KEY))
    keyboard.add(types.KeyboardButton(text = SHOW_ALL_KANJI_KEY))
    keyboard.add(types.KeyboardButton(text = IMPORT_EXCEL_KEY))
    keyboard.add(types.KeyboardButton(text = IMPORT_TXT_KEY))
    keyboard.add(types.KeyboardButton(text = EXPORT_EXCEL_KEY))
    keyboard.add(types.KeyboardButton(text = EXPORT_TXT_KEY))
    keyboard.add(types.KeyboardButton(text = LOAD_RADICAL_TABLE_EXCEL_KEY))
    keyboard.add(types.KeyboardButton(text = LOAD_RADICAL_TABLE_TXT_KEY))
    keyboard.add(types.KeyboardButton(text = LINK_KANJI_TO_RADICAL_KEY))
    bot.send_message(message.chat.id,
                     "Select your next doing",
                     reply_markup = keyboard)
    
def SaveKanji(message, isRadical):
    SaveKanjiProcess(message, isRadical)

def ShowAddKanjiDisplay(message, isRadical = False):
    template_message = """
Fill dates in the next template:\n
KANJI: <Kanji>
PATH_TO_IMAGE: <Path_To_Image>
ONYOMI: <listOfOnyomi>
ONY_LATIN: <listOfOnyomiLatin>
KUNYOMI: <listOfKunyomi>
KUNY_LATIN: <listOfKunyomiLatin>
RU: <listOfRuTranslate>
EN: <listOfEnTranslate>
Way doesn't mean"""
    msg = bot.send_message(message.chat.id,
                     template_message)
    bot.register_next_step_handler(msg, SaveKanji, isRadical)

def SaveKanjiProcess(message, isRadical):
    kanjiDict = parse_kanji_text(message.text)
    answer = SendToBase(kanjiDict)
    if isRadical:
        answer = SendRadicalToBase(kanjiDict["kanji"])
    bot.send_message(message.chat.id,
                     answer) 
    
def ShowAllKanjiDisplay(message):
    kanjies = select_all_kanji()
    answer = ""
    for each in kanjies:
        answer += each[0] + ", "
    bot.send_message(message.chat.id,
                     answer[:-2])

def ReadingFile(message, isRadical):
    file_info = bot.get_file(message.document.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    with open(path_to_folder + message.document.file_name, "wb") as f:
        f.write(downloaded_file)
    bot.reply_to(message, "File was getting successful. I'm reading it.")
    if file_info.file_path[-4:] == ".txt":
        answer = read_txt(path_to_folder + message.document.file_name, isRadical)
    else:
        answer = read_excel(path_to_folder + message.document.file_name, isRadical)
    bot.send_message(message.chat.id,
                     answer)

def DownloadFile(message, isRadical):
    ReadingFile(message, isRadical)

def ImportExcelDisplay(message, isRadical = False):
    msg = bot.send_message(message.chat.id,
                     "Send me excel file, please")
    bot.register_next_step_handler(msg, DownloadFile, isRadical)

def ImportTxtDisplay(message, isRadical = False):
    msg = bot.send_message(message.chat.id,
                           "Send me a txt file, please")
    bot.register_next_step_handler(msg, DownloadFile, isRadical)

def ReadKanjiFromUser(message):
    kanjiDict = read_kanji_from_user(message.text)
    answer = """
        Kanji: {}
        onyomi: {}
        kunyomi: {}
        eng: {}
        rus: {}    
    """.format(kanjiDict["kanji"],
               kanjiDict["onyomi"],
               kanjiDict["kunyomi"],
               kanjiDict["eng"],
               kanjiDict["rus"])
    path_to_kanji = getcwd() + "{}.png".format(kanjiDict["kanji"])
    create_kanji_image(kanjiDict["kanji"], path_to_kanji)
    bot.send_message(message.chat.id,
                     answer)
    with open(path_to_kanji, "rb") as file:
        bot.send_photo(
            message.chat.id,
            file
        )

def ShowKanjiDisplay(message):
    msg = bot.send_message(message.chat.id,
                           "Send me any kanji, please")
    bot.register_next_step_handler(msg, ReadKanjiFromUser)

def ReadAllKanji(ext):
    kanjiList = select_all_kanji()
    if ext == "xls":
        path_to_export = put_kanji_in_excel(kanjiList)
    else:
        path_to_export = put_kanji_in_txt(kanjiList)
    return path_to_export

def ExportExcelDisplay(message):
    path_to_export = ReadAllKanji("xls")
    with open(path_to_export, "rb") as file:
        bot.send_document(
            message.chat.id,
            file
        )

def ExportTXTDisplay(message):
    path_to_export = ReadAllKanji("txt")
    with open(path_to_export, "rb") as file:
        bot.send_document(
            message.chat.id,
            file
        )

def LinkingKanjiWithRadicals(message):
    answer = MakeLinkWithRadical(message.text)
    bot.send_message(
        message.chat.id,
        text = answer
    )

def LinkKanjiToRadicalDisplay(message):
    template = """
    Send me message as:
    link <Kanji> <Radicals>
    """
    msg = bot.send_message(
        message.chat.id,
        text = template
    )
    bot.register_next_step_handler(msg, LinkingKanjiWithRadicals)

# Client
def ShowDisplayClientMode(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard = True)
    keyboard.add(types.KeyboardButton(text = QUIZ_KEY))
    keyboard.add(types.KeyboardButton(text = TYPING_KEY))
    keyboard.add(types.KeyboardButton(text = LEARN_NEW_KEY))
    keyboard.add(types.KeyboardButton(text = RECORDS_KEY))
    keyboard.add(types.KeyboardButton(text = STATS_KEY))
    bot.send_message(message.chat.id,
                    "Select your next doing, please",
                    reply_markup = keyboard)
    
def ShowQuizDisplay(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard = True)
    keyboard.add(types.KeyboardButton(text = KANJI_TO_ONYOMI_KEY))
    keyboard.add(types.KeyboardButton(text = ONYOMI_TO_KANJI_KEY))
    keyboard.add(types.KeyboardButton(text = KANJI_TO_KUNYOMI_KEY))
    keyboard.add(types.KeyboardButton(text = KUNYOMI_TO_KANJI_KEY))
    keyboard.add(types.KeyboardButton(text = KANJI_TO_ENG_KEY))
    keyboard.add(types.KeyboardButton(text = ENG_TO_KANJI_KEY))
    keyboard.add(types.KeyboardButton(text = KANJI_TO_RUS_KEY))
    keyboard.add(types.KeyboardButton(text = RUS_TO_KANJI_KEY))
    bot.send_message(message.chat.id,
                     "Which quiz do you want?",
                     reply_markup = keyboard)