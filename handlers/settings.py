from bot_instance import bot
from constants import *
from ui.settings import (
    ShowSetLevelDisplay
)
@bot.message_handler(func = lambda message: message.text == LEVEL_KEY)
def SetLevel(message):
    ShowSetLevelDisplay(message)