from developer import (
    AddOnyomi,
    AddKunyomi,
    AddKanji,
    AddRadical,
    AddKanjiMeaning
)
from database import (
    add_word,
    add_word_meaning,
    add_word_reading
)
from models import Kanji
from itertools import zip_longest

def SendToBase(kanjiDict):
    try:
        kanji = Kanji()
        kanji.hieroglyph = kanjiDict["kanji"]
        kanji.path_to_image = kanjiDict["path_to_image"]
        kanji_id = AddKanji(kanji)
        for ru, en in zip_longest(kanjiDict["ru"], kanjiDict["en"]):
            kanji.rus, kanji.eng = ru, en
            AddKanjiMeaning(kanji_id, kanji)
        for onyomi, latin in zip_longest(kanjiDict["onyomi"], kanjiDict["ony_latin"]):
            kanji.onyomi, kanji.ony_latin = onyomi, latin
            AddOnyomi(kanji_id, kanji)
        for kunyomi, latin in zip_longest(kanjiDict["kunyomi"], kanjiDict["kuny_latin"]):
            kanji.kunyomi, kanji.kuny_latin = kunyomi, latin
            AddKunyomi(kanji_id, kanji)
        return "Successful"
    except Exception as ex:
        return ex

def SendRadicalToBase(radical: str):
    try:
        radical_id = AddRadical(radical)
        return "Successfull. Radical is number {} save".format(radical_id)
    except Exception as ex:
        return ex
    
def SendWordToBase(wordDict):
    try:
        word_id = add_word(wordDict["word"][0])
        for reading in wordDict["reading"]:
            add_word_reading(word_id, reading)
        for eng, rus in zip_longest(wordDict["eng"], wordDict["rus"]):
            add_word_meaning(word_id, eng, rus)
        return "Successful"
    except Exception as ex:
        return ex