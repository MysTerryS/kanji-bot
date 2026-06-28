from random import choice
from models import Kanji
from database import (SelectUser, AddUser, 
                      SelectKanjiForUser, InsertKanjiToUser, 
                      SelectRadicalsForUser, InsertRadicalToUser,
                      select_radical, select_kanji,
                      SelectKanjiForSelect,
                      SelectRadicalForSelect,
                      SetStatusRadical
)
def CheckUser(user_id):
    user = SelectUser(user_id)
    if user == None:
        user = AddUser(user_id)
    return user

def UserToRadical(user_id, status, level):
    radicalIds = SelectRadicalsForUser(user_id, status)
    if radicalIds == None:
        MadeAvailable(user_id, level)
        radicalIds = SelectRadicalsForUser(user_id, status)
    radicalList = list()
    for radical in radicalIds:
        radicalList.append(select_radical(radical[0], True))
    return radicalList
    
def SelectLearnRadical(user_id, radical):
    radical_id = select_radical(radical)
    kanjiIDs = SelectKanjiForSelect(user_id, radical_id)
    kanjiList = list()
    if kanjiIDs:
        for kanji in kanjiIDs:
            kanjiList.append(select_kanji(kanji[0], True))
    if radical not in kanjiList:
        kanjiList.append(radical)
    return kanjiList

def SelectLearnKanji(user_id, kanji):
    kanjiObject = Kanji()
    kanjiObject.hieroglyph = kanji
    kanji_id = select_kanji(kanjiObject)
    InsertKanjiToUser(user_id, kanji_id, 0)

def MadeAvailable(user_id, level):
    radicalList = SelectRadicalForSelect(user_id, level)
    for radical in radicalList:
        InsertRadicalToUser(user_id, radical[0], 0)