from bot_instance import bot
from constants import *
from ui.main_menu import BackToPrevious
@bot.message_handler(func = lambda message: message.text == CANCEL_KEY)
def Cancel(message):
    BackToPrevious(message)