from os import remove, getcwd
from services.parser import parse_kanji_text
from services.import_service import SendToBase, SendRadicalToBase
from services.info import ShowKanjiWithPronouncesAndMeaning, SafeJoin
from models import Kanji

path_to_txt = getcwd() + "kanjiList.txt"

def read_file(path_to_file):
    with open(path_to_file, mode = "r", encoding = "utf-8") as f:
        data = f.read()
    return data

def read_txt(path_to_file, isRadical):
    data = read_file(path_to_file)
    lines = data.split("\n\n")
    try:
        for line in lines:
            kanjiDict = parse_kanji_text(line)
            SendToBase(kanjiDict)
            if isRadical:
                SendRadicalToBase(kanjiDict["kanji"])
        return "Successful"
    except Exception as ex:
        return ex

def one_kanji(file, kanjiDict):
    file.write("Kanji: " + kanjiDict["kanji"] + "\n")
    file.write("Onyomi: " + SafeJoin(kanjiDict["onyomi"]) + "\n")
    file.write("Ony_latin: " + SafeJoin(kanjiDict["ony_latin"]) + "\n")
    file.write("Kunyomi: " + SafeJoin(kanjiDict["kunyomi"]) + "\n")
    file.write("Kuny_latin: " + SafeJoin(kanjiDict["kuny_latin"]) + "\n")
    file.write("English: " + SafeJoin(kanjiDict["eng"]) + "\n")
    file.write("Russian: " + SafeJoin(kanjiDict["rus"]) + "\n")
    file.write("\n")
    
def put_kanji_in_txt(kanjiList):
    with open(path_to_txt, mode = "w+", encoding = "utf-8") as file:
        for kanji in kanjiList:
            kanjiObject = Kanji()
            kanjiObject.hieroglyph = kanji[0]
            kanjiDict = ShowKanjiWithPronouncesAndMeaning(kanjiObject)
            one_kanji(file, kanjiDict)
    return path_to_txt