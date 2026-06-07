# Add
    # Kanji
    # translate
        # English
        # Russian
    # onyomi
        # katakana
        # latin
    # kunyomi
        # hiragana
        # latin
    # image
# ShowAll
# Show(Kanji)
# Users
# Возможно добавлю механизм связанный с радикалами, т.е. можно добавлять кандзи
# у которых будет единый радикал и так можно заучивать это
# связано будет с клиентом больше
# Radicals table
# link with radicals
# kanji on radicals

import sqlite3
from database import *
from models import Kanji
conn = sqlite3.connect("kanji_base.db", check_same_thread = False)

# Developer

def AddKanji(kanji: Kanji):
    kanji_id = select_kanji(kanji)
    if kanji_id == None:
        kanji_id = insert_kanji(kanji)
    return kanji_id

def AddRadical(radical: str):
    radical_id = select_radical(radical)
    if radical_id == None:
        radical_id = insert_radical(radical)
    return radical_id

def AddKanjiMeaning(kanji_id: int, kanji: Kanji):
    insert_meaning_kanji(kanji_id, kanji)

def AddOnyomi(kanji_id: int, kanji: Kanji):
    insert_onyomi(kanji_id, kanji)

def AddKunyomi(kanji_id: int, kanji: Kanji):
    insert_kunyomi(kanji_id, kanji)

def ShowKanji(kanji):
    return select_kanji(kanji)