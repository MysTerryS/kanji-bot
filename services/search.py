from database import (
    select_kanji_by_kunyomi,
    select_kanji_by_onyomi,
    select_kanji,
    select_radicals_for_kanji,
    select_radical,
    select_all_of_radical_kanji,
    link_radical
)
from models import Kanji

def MakeKanjiFromOnyomi(onyomi):
    kanji_ids = select_kanji_by_onyomi(onyomi)
    if not kanji_ids:
        return None
    kanjies = list()
    for kanji_id in kanji_ids:
        kanjies.append(select_kanji(kanji_id, True))
    return kanjies

def MakeKanjiFromKunyomi(kunyomi):
    kanji_ids = select_kanji_by_kunyomi(kunyomi)
    if not kanji_ids:
        return None
    kanjies = list()
    for kanji_id in kanji_ids:
        kanjies.append(select_kanji(kanji_id[0], True))
    return kanjies

def RadicalsFromKanji(hieroglyph):
    kanji = Kanji()
    kanji.hieroglyph = hieroglyph
    kanji_id = select_kanji(kanji)
    radical_ids = select_radicals_for_kanji(kanji_id)
    radicals = ""
    for radical_id in radical_ids:
        radicals += select_radical(radical_id[0], True) + ", "
    return radicals[:-2]

def GetRadicalsKanji():
    table = select_all_of_radical_kanji()
    radicalKanjiDict = dict()
    for radical_id, kanji_ids in table:
        key = select_radical(radical_id, True)
        radicalKanjiDict[key] = ""
        kanjies = kanji_ids.split(",")
        for kanji_id in kanjies:
            kanji = select_kanji(kanji_id, True)
            radicalKanjiDict[key] += kanji + ", "
        radicalKanjiDict[key] = radicalKanjiDict[key][:-2]
    return radicalKanjiDict

def GetKanjiID(hieroglyph: str):
    kanji = Kanji()
    kanji.hieroglyph = hieroglyph
    kanji_id = select_kanji(kanji)
    return kanji_id

def GetRadicalID(radical: str):
    return select_radical(radical)

def MakeLinkWithRadical(text: str):
    text = text.split(" ")
    hieroglyph, *radicals = text[1:]
    kanji_id = GetKanjiID(hieroglyph)
    try:
        for radical in radicals:
            radical_id = GetRadicalID(radical)
            link_radical(kanji_id, radical_id)
        return "Successful"
    except Exception as ex:
        return ex