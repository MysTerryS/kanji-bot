import sqlite3
from models import Kanji

conn = sqlite3.connect("kanji_base.db", check_same_thread = False)

def insert_kanji(kanji: Kanji):
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO kanji (
                   hieroglyph,
                   path_to_image
                   ) VALUES (?, ?)
    """, (kanji.hieroglyph,
          kanji.path_to_image,
          ))
    conn.commit()
    return cursor.lastrowid

def insert_radical(radical: str):
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO radicals (
                   hieroglyph
                   ) VALUES (?)
    """, (radical,))
    conn.commit()
    return cursor.lastrowid

def insert_meaning_kanji(kanji_id: int, kanji: Kanji):
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO kanji_meanings (
                   kanji_id,
                   eng,
                   rus
                   ) VALUES (?, ?, ?)   
    """, (kanji_id,
          kanji.eng,
          kanji.rus,))
    conn.commit()

def insert_onyomi(kanji_id: int, kanji: Kanji):
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO onyomi (
                   kanji_id,
                   reading,
                   latin
                   ) VALUES (?, ?, ?) 
    """, (kanji_id,
          kanji.onyomi,
          kanji.ony_latin,))
    conn.commit()

def insert_kunyomi(kanji_id: int, kanji: Kanji):
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO kunyomi (
                   kanji_id,
                   reading,
                   latin
                   ) VALUES (?, ?, ?)
    """, (kanji_id,
          kanji.kunyomi,
          kanji.kuny_latin,))
    conn.commit()

def select_kanji(kanji: Kanji | int, isKanji = False):
    cursor = conn.cursor()
    cursor.execute("""
        SELECT {} FROM kanji
                   WHERE {} = ?
    """.format("id" if not isKanji else "hieroglyph", "hieroglyph" if not isKanji else "id"), (kanji.hieroglyph if not isKanji else kanji,))
    res = cursor.fetchone()
    return res[0] if res else None

def select_kanji_by_onyomi(onyomi: str):
    cursor = conn.cursor()
    cursor.execute("""
        SELECT kanji_id FROM onyomi
            WHERE reading = ?
    """, (onyomi,))
    res = cursor.fetchall()
    return res if res else None

def select_kanji_by_kunyomi(kunyomi: str):
    cursor = conn.cursor()
    cursor.execute("""
        SELECT kanji_id FROM kunyomi
            WHERE reading = ?
    """, (kunyomi,))
    res = cursor.fetchall()
    return res if res else None

def select_all_kanji():
    cursor = conn.cursor()
    cursor.execute("""
        SELECT hieroglyph FROM kanji
    """)
    res = cursor.fetchall()
    return res

def select_kanji_all_meanings(id: int):
    cursor = conn.cursor()
    cursor.execute("""
        SELECT eng, rus FROM kanji_meanings
            WHERE kanji_id = ?
    """, (id,))
    res = cursor.fetchall()
    return res

def select_kanji_all_onyomi(id: int):
    cursor = conn.cursor()
    cursor.execute("""
        SELECT reading, latin FROM onyomi
            WHERE kanji_id = ?
    """, (id,))
    res = cursor.fetchall()
    return res

def select_kanji_all_kunyomi(id: int):
    cursor = conn.cursor()
    cursor.execute("""
        SELECT reading, latin FROM kunyomi
            WHERE kanji_id = ?
    """, (id,))
    res = cursor.fetchall()
    return res

def select_radical(radical: int | str, isHieroglyph = False):
    cursor = conn.cursor()
    cursor.execute("""
        SELECT {} FROM radicals
            WHERE {} = ?
    """.format("id" if not isHieroglyph else "hieroglyph", "hieroglyph" if not isHieroglyph else "id"), (radical,))
    res = cursor.fetchone()
    return res[0] if res else None

def link_radical(kanji_id: int, radical_id: int):
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO kanji_radicals (
            kanji_id,
            radical_id) VALUES (?, ?)
    """, (kanji_id, radical_id))
    conn.commit()

def select_all_of_radical_kanji():
    cursor = conn.cursor()
    cursor.execute("""
        SELECT 
            radical_id,
            GROUP_CONCAT(kanji_id)
        FROM kanji_radicals
        GROUP BY radical_id
    """)
    res = cursor.fetchall()
    return res

def select_radicals_for_kanji(kanji_id):
    cursor = conn.cursor()
    cursor.execute("""
        SELECT
            radical_id
        FROM kanji_radicals
        WHERE kanji_id = ?
    """, (kanji_id,))
    res = cursor.fetchall()
    return res

def AddUser(user_id: int):
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO users (
                   id)
                VALUES (?)
    """, (user_id,))
    conn.commit()
    return cursor.lastrowid

def SelectUser(user_id: int):
    cursor = conn.cursor()
    cursor.execute("""
        SELECT
            1
        FROM users
            WHERE id = ?
    """, (user_id,))
    res = cursor.fetchone()
    return res[0] if res else None

def InsertRadicalToUser(user_id: int, radical_id: int, status: int):
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO user_radicals (
                user_id, radical_id, status)
                VALUES (?, ?, ?)
    """, (user_id, radical_id, status,))
    conn.commit()
    return cursor.lastrowid

def SelectRadicalsForUser(user_id: int, status: int):
    cursor = conn.cursor()
    cursor.execute("""
        SELECT radical_id
        FROM user_radicals
        WHERE user_id = ? and status = ?
        """, (user_id, status,))
    res = cursor.fetchall()
    return res if res else None

def SelectKanjiCount(user_id: int):
    cursor = conn.cursor()
    cursor.execute("""
        SELECT count(kanji_id)
        FROM user_kanji
        WHERE user_id = ?
    """,(user_id,))
    res = cursor.fetchone()
    return res[0] if res else None

def InsertKanjiToUser(user_id: int, kanji_id: int, status: int):
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO user_kanji (
            user_id, kanji_id, status)
            VALUES (?, ?, ?)
    """, (user_id, kanji_id, status,))
    conn.commit()
    return cursor.lastrowid

def SelectKanjiForUser(user_id: int, status: int):
    cursor = conn.cursor()
    cursor.execute("""
        SELECT kanji_id
        FROM user_kanji
        WHERE user_id = ? and status = ?
    """, (user_id, status,))
    res = cursor.fetchall()
    return res if res else None

def SelectKanjiForSelect(user_id: int, radical_id: int):
    cursor = conn.cursor()
    cursor.execute("""
        SELECT k.id, k.hieroglyph
        FROM kanji k
        JOIN kanji_radicals kr
            ON kr.kanji_id = k.id
        LEFT JOIN user_kanji uk
            ON uk.kanji_id = k.id
            AND uk.user_id = ?
        WHERE kr.radical_id = ?
            AND uk.kanji_id IS NULL
    """, (user_id, radical_id))
    res = cursor.fetchall()
    return res if res else None

def SelectRadicalForSelect(user_id: int, level = 1):
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, hieroglyph
        FROM radicals
        WHERE id NOT IN (
            SELECT radical_id
            FROM user_radicals
            WHERE user_id = ?)
        AND level = ?
        ORDER BY RANDOM()
        LIMIT 5
    """, (user_id, level,))
    res = cursor.fetchall()
    return res if res else None

def SetStatusRadical(user_id: int, radical_id: int, status: int):
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE user_radicals
        SET status = ?
        WHERE user_id = ? and radical_id = ?
    """, (status, user_id, radical_id))
    conn.commit()

def SetStatusKanji(user_id: int, kanji_id: int, status: int):
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE user_kanji
        SET status = ?
        WHERE user_id = ? and kanji_id = ?
    """, (status, user_id, kanji_id))
    conn.commit()

def DeleteRadicalFromUser(user_id: int, radical_id: int):
    cursor = conn.cursor()
    cursor.execute("""
        DELETE FROM user_radicals
        WHERE user_id = ? and radical_id = ?
    """, (user_id, radical_id))
    conn.commit()

def UpdateKanjiForUser(user_id: int, kanji_id: int, isCorrect: bool):
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE user_kanji
        SET {0} = {0} + 1
        WHERE user_id = ? and kanji_id = ?               
    """.format("correct" if isCorrect else "wrong"), (user_id, kanji_id))
    conn.commit()

def add_word(word: str):
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO words (
                word)
            VALUES (?)
    """, (word,))
    conn.commit()
    return cursor.lastrowid

def add_word_reading(word_id: int, reading: str):
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO word_readings (
            word_id, reading)
            VALUES (?, ?)
    """, (word_id, reading,))
    conn.commit()

def add_word_meaning(word_id: int, eng: str, rus: str):
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO word_meanings (
            word_id, eng, rus)
            VALUES (?, ?, ?)
    """, (word_id, eng, rus,))
    conn.commit()