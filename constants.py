# PathToFiles
from os import getcwd
path_to_folder = getcwd()
path_to_export = getcwd() + "KanjiList.xls"

# ModeDisplay
DEV_KEY = "Developer"
CLI_KEY = "Client"
SETTINGS_KEY = "Settings"

# DeveloperMode
ADD_KANJI_KEY = "/addkanji"
ADD_RADICAL_KEY = "/addradical"
LINK_KANJI_TO_RADICAL_KEY = "/link_kanji_to_radical"
SHOW_KANJI_KEY = "/showkanji"
SHOW_ALL_KANJI_KEY = "/showallkanji"
IMPORT_EXCEL_KEY = "/import_excel"
IMPORT_TXT_KEY = "/import_txt"
EXPORT_EXCEL_KEY = "/export_excel"
EXPORT_TXT_KEY = "/export_txt"
LOAD_RADICAL_TABLE_EXCEL_KEY = "/load_radical_table_excel"
LOAD_RADICAL_TABLE_TXT_KEY = "/load_radical_table_txt"
LOAD_LINKS_TABLE_KEY = "/load_links_table"
EXPORT_KANJI_RADICALS_KEY = "/export_kanji_with_radicals"
ADD_WORD_KEY = "/add_word"
#SHARE_KANJI_TO_RADICALS_KEY = "/share_kanji_to_radicals"

# ClientMode
QUIZ_KEY = "/quiz"
KANJI_TO_ONYOMI_KEY = "/kanji_to_onyomi"
ONYOMI_TO_KANJI_KEY = "/onyomi_to_kanji"
KANJI_TO_KUNYOMI_KEY = "/kanji_to_kunyomi"
KUNYOMI_TO_KANJI_KEY = "/kunyomi_to_kanji"
KANJI_TO_ENG_KEY = "/kanji_to_eng"
ENG_TO_KANJI_KEY = "/eng_to_kanji"
KANJI_TO_RUS_KEY = "/kanji_to_rus"
RUS_TO_KANJI_KEY = "/rus_to_kanji"
TYPING_KEY = "/typing"
LEARN_NEW_KEY = "/learn_new"
LEARN_BY_RADICAL_NEW_KEY = "/by_radical"
SEARCH_KANJI_KEY = "/search_kanji"
SEARCH_BY_ONYOMI_KEY = "/search_by_onyomi"
SEARCH_BY_KUNYOMI_KEY = "/search_by_kunyomi"
LEARN_NEW_WORDS_KEY = "/words"
RECORDS_KEY = "/records"
STATS_KEY = "/stats"
HARDEST_KEY = "/hardest"
CORRECT_KEY = "/correct"
ERRORS_KEY = "/errors"
FINISH_KEY = "/finish"
CONTINUE_KEY = "/continue"
UPDATE_KEY = "/update"

# Settings
LEVEL_KEY = "/set_level"
BEGINNER_KEY = "/beginner"
INTERMEDIATE_KEY = "/intermediate"
ADVANCED_KEY = "/advanced"

# Common
CANCEL_KEY = "/cancel"
YES_KEY = "/yes"
NO_KEY = "/no"

LEVELS = {
    BEGINNER_KEY: 1,
    INTERMEDIATE_KEY: 2,
    ADVANCED_KEY: 3
}