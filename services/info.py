from models import Kanji
from database import (
    select_kanji,
    select_kanji_all_kunyomi,
    select_kanji_all_onyomi,
    select_kanji_all_meanings
)
from services.search import RadicalsFromKanji

def ShowKanjiWithPronouncesAndMeaning(kanji):
    id = select_kanji(kanji)
    if id == None:
        return None
    kanjiDict = dict()
    kanjiDict["kanji"] = kanji.hieroglyph
    onyomiList = select_kanji_all_onyomi(id)
    onyomi = list()
    ony_latin = list()
    for line in onyomiList:
        onyomi.append(line[0])
        ony_latin.append(line[1])
    kanjiDict["onyomi"] = onyomi
    kanjiDict["ony_latin"] = ony_latin 
    kunyomiList = select_kanji_all_kunyomi(id)
    kunyomi = list()
    kuny_latin = list()
    for line in kunyomiList:
        kunyomi.append(line[0])
        kuny_latin.append(line[1])
    kanjiDict["kunyomi"] = kunyomi
    kanjiDict["kuny_latin"] = kuny_latin
    meanings = select_kanji_all_meanings(id)
    eng, rus = list(), list()
    for row in meanings:
        eng.append(row[0])
        rus.append(row[1])
    kanjiDict["eng"], kanjiDict["rus"] = eng, rus
    return kanjiDict

def InfoAboutKanji(kanji, isQuiz = False):
    kanjiDict = read_kanji_from_user(kanji)
    radicals = RadicalsFromKanji(kanji)
    answer = ""
    if not isQuiz:
        answer = "Kanji: {}".format(SafeJoin(kanjiDict["kanji"]))
    answer = answer + """

        onyomi: {}
        kunyomi: {}

        eng: {}
        rus: {}

        radicals: {}    
    """.format(SafeJoin(kanjiDict["onyomi"]),
               SafeJoin(kanjiDict["kunyomi"]),
               SafeJoin(kanjiDict["eng"]),
               SafeJoin(kanjiDict["rus"]),
               radicals)
    return answer

def SafeJoin(element):
    if not element:
        return ""
    return ", ".join(str(x) for x in element if x is not ModuleNotFoundError and x is not None)
    
def read_kanji_from_user(text: str):
    kanji = Kanji()
    kanji.hieroglyph = text
    kanjiDict = ShowKanjiWithPronouncesAndMeaning(kanji)
    return kanjiDict