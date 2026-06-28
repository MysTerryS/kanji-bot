from bot_instance import bot
from constants import *

from os import getcwd

from services.parser import parse_kanji_text
from services.import_service import SendRadicalToBase, SendToBase, SendWordToBase
from services.info import InfoAboutKanji
from services.image import create_kanji_image
from services.search import MakeLinkWithRadical, GetRadicalsKanji, RadicalsFromKanji

from database import select_all_kanji

from inpout.excel_export import put_kanji_in_excel, make_all_of_radical_table
from inpout.excel_import import read_excel, read_links_excel

from txt import read_txt, put_kanji_in_txt

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

def ShowAddWordDisplay(message):
    template_message = """
Fill dates in the next template:\n
WORD: <Word>
READING: <listOfReading>
ENG: <listOfEngTranslate>
RUS: <listOfRusTranslate>
Way doesn't mean
"""
    msg = bot.send_message(
        message.chat.id,
        template_message)
    bot.register_next_step_handler(msg, SaveWord)

def SaveWord(message):
    SaveWordProcess(message)

def SaveWordProcess(message):
    wordDict = parse_kanji_text(message.text)
    answer = SendWordToBase(wordDict)
    bot.send_message(
        message.chat.id,
        answer
    )

def SaveKanji(message, isRadical):
    SaveKanjiProcess(message, isRadical)

def SaveKanjiProcess(message, isRadical):
    kanjiDict = parse_kanji_text(message.text)
    answer = SendToBase(kanjiDict)
    if isRadical:
        answer = SendRadicalToBase(kanjiDict["kanji"])
    bot.send_message(message.chat.id,
                     answer)
    
def ShowKanjiDisplay(message):
    msg = bot.send_message(message.chat.id,
                           "Send me any kanji, please")
    bot.register_next_step_handler(msg, ReadKanjiFromUser)

def ReadKanjiFromUser(message):
    answer = InfoAboutKanji(message.text)
    path_to_kanji = getcwd() + "{}.png".format(message.text)
    create_kanji_image(message.text, path_to_kanji)
    bot.send_message(message.chat.id,
                     answer)
    with open(path_to_kanji, "rb") as file:
        bot.send_photo(
            message.chat.id,
            file
        )

def GetSharingKanji(message):
    answer = RadicalsFromKanji(message.text)
    bot.send_message(
        message.chat.id,
        text = answer
    )

def ShareKanjiDisplay(message):
    msg = bot.send_message(
        message.chat.id,
        text = "Send me a kanji, please."
    )
    bot.register_next_step_handler(msg, GetSharingKanji)

def ImportExcelDisplay(message, isRadical = False):
    msg = bot.send_message(message.chat.id,
                     "Send me excel file, please")
    bot.register_next_step_handler(msg, DownloadFile, isRadical)

def ImportTxtDisplay(message, isRadical = False):
    msg = bot.send_message(message.chat.id,
                           "Send me a txt file, please")
    bot.register_next_step_handler(msg, DownloadFile, isRadical)

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

def ReadAllKanji(ext):
    kanjiList = select_all_kanji()
    if ext == "xls":
        path_to_export = put_kanji_in_excel(kanjiList)
    else:
        path_to_export = put_kanji_in_txt(kanjiList)
    return path_to_export

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

def LoadRadicalTable(message):
    radicalKanjiDict = GetRadicalsKanji()
    path_to_export = make_all_of_radical_table(radicalKanjiDict)
    with open(path_to_export, "rb") as file:
        bot.send_document(
            message.chat.id,
            file
        )

def ReadingLinks(message):
    file_info = bot.get_file(message.document.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    with open(path_to_folder + message.document.file_name, "wb") as f:
        f.write(downloaded_file)
    bot.reply_to(message, "File was getting successful. I'm reading it.")
    #if file_info.file_path[-4:] == ".xls":
    answer = read_links_excel(path_to_folder + message.document.file_name)
    #else:
        #answer = read_excel(path_to_folder + message.document.file_name, isRadical)
    bot.send_message(message.chat.id,
                     answer)

def ImportLinksTableDisplay(message):
    msg = bot.send_message(
        message.chat.id,
        text = "Send me a file with links, please"
    )
    bot.register_next_step_handler(msg, ReadingLinks)