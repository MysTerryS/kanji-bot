from random import choice
from database import SelectKanjiForUser, select_kanji
from services.info import read_kanji_from_user

def RandomKanji(user_id, status):
    requestIds = SelectKanjiForUser(user_id, status)
    request = [select_kanji(kanji[0], True) for kanji in requestIds]
    kanjies = [kanji[0] for kanji in request]
    return choice(kanjies)

def SelectRandomKanji(mode, user_id, status, isTyping = False):
    if not isTyping:
        while True:
            kanjiList = [RandomKanji(user_id, status) for i in range(4)]
            modes = {}
            for kanji in kanjiList:
                values = ModeFromKanji(kanji, mode)[1]
                if not values:
                    break
                modes[kanji] = choice(values)
            if None in modes.values():
                modes.clear()
            if len(modes) == 4:
                break
        return (kanjiList, modes)
    else:
        value = None
        while not value:
            kanji = RandomKanji(user_id, status)
            value = ModeFromKanji(kanji, mode)[1]
        return (kanji, value)
    
def ModeFromKanji(kanji, mode):
    out = read_kanji_from_user(kanji)
    return (kanji, out[mode])