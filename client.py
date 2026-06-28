# mykanji(list)
# train
    # Kanji to onyomi(with options)
        # katakana
        # latin
    # Kanji to kunyomi(with options)
        # hiragana
        # latin
    # Kanji to translate(with options)
        # English
        # Russian
    # Kanji typing
        # onyomi
            # katakana
            # latin
        # kunyomi
            # hiragana
            # latin
        # english
        # russian
# learn_new
# records
# stats
    # hardest(need to learn more)
    # correct(without errors)
    # wrong(error)

"""
    User choose the mode from kanji or typing.
    If it is kanji -> onyomi            -> one variable with type
                        latin
                    kunyomi
                        latin
                    meaning
                        eng
                        rus
        if is typing <- onyomi          -> one variable with type
                            latin
                        kunyomi
                            latin
                        meaning
                            eng
                            rus
                    -> kanji 
"""
"""
1. Система проверяет есть ли у пользователя доступные радикалы для обучения.
2. Если их нет, то она создает группу 5 радикалов доступными для обучения.
3. Пользователь выбирает любой из этих радикалов, учит их и получает доступ к другим
    кандзи, связанные с этими радикалами.
4. Когда пользователь выбирает выучить новые кандзи, система выводит радикалы
    такие что не встречались для него ранее.
5. Пользователь учит кандзи и радикалы через Quiz или typing.
6. Когда он выучит их, открывается доступ к другим.
status
0 - доступен для обучения
1 - изучается
2 - изучен

Добавить выбор уровня сложности радикала(1, 2, 3)

27.06.2026 - добавить функцию проверки chat_id при перезапуске,
т.е. пользователь ввел кнопку, бот вылетит от этого, надо чтобы он по chat_id
пересоздавал user_state.
"""