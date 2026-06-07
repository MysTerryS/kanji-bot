# Kanji-object
class Kanji:
    hieroglyph: str
    onyomi: str
    ony_latin: str
    kunyomi: str
    kuny_latin: str
    eng: str
    rus: str
    path_to_image: str
    
    def check_onyomi(self, answer: str):
        return self.onyomi == answer
    
    def check_kunyomi(self, answer: str):
        return self.kunyomi == answer
    
    def check_eng(self, answer):
        return self.eng == answer
    
    def check_rus(self, answer):
        return self.rus == answer