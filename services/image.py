from PIL import Image, ImageDraw, ImageFont
import os

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