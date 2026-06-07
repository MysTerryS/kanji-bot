from itertools import zip_longest
from developer import *
from PIL import Image, ImageDraw, ImageFont
import os

def SaveValue(key, value):
    if key in ["ru", "en", "onyomi", "ony_latin",
        "kunyomi", "kuny_latin"]:
        if value is None:
            return []
        return [item.strip() for item in value.split(",")]
        
    return value

def parse_kanji_text(text: str) -> dict:
    result = {}
    lines = text.splitlines()
    for line in lines:
        if not line.strip():
            continue
        key, value = line.split(":", 1)
        key = key.strip().lower()
        value = value.strip()
        result[key] = SaveValue(key, value)
    return result

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
    
def read_kanji_from_user(text: str):
    kanji = Kanji()
    kanji.hieroglyph = text
    kanjiDict = ShowKanjiWithPronouncesAndMeaning(kanji)
    return kanjiDict

def create_kanji_image(kanji: str, path: str):
    img = Image.new("RGB", (300, 300), "white")
    draw = ImageDraw.Draw(img)

    #font = ImageFont.truetype("fonts/NotoSansJP-Bold.ttf", 180)
    font = ImageFont.truetype("YuGothM.ttc", 180)
    bbox = draw.textbbox((0, 0), kanji, font = font)
    x = (300 - (bbox[2] - bbox[0])) / 2
    y = (300 - (bbox[3] - bbox[1])) / 2 - 20

    draw.text((x, y), kanji, fill = "black", font = font)

    os.makedirs(os.path.dirname(path), exist_ok = True)
    img.save(path)

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