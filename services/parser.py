def SaveValue(key, value):
    if key in ["ru", "en", "onyomi", "ony_latin",
        "kunyomi", "kuny_latin", "word", "reading", "rus", "eng"]:
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