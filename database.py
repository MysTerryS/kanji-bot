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

def select_kanji(kanji: Kanji):
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id FROM kanji
                   WHERE hieroglyph = ?
    """, (kanji.hieroglyph,))
    res = cursor.fetchone()
    return res[0] if res else None

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

def select_radical(radical: str):
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id FROM radicals
            WHERE hieroglyph = ?
    """, (radical,))
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