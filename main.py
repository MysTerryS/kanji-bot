from constants import *
from bot_instance import bot
from ui.main_menu import (
    ShowModeDisplay,
    ShowDeveloperMode,
    ShowDisplayClientMode
)
from ui.settings import (
    SettingsDisplay
)
import handlers.client
import handlers.developer
import handlers.common
import handlers.settings

@bot.message_handler(commands = ["start"])
def StartMessaging(message):
    ShowModeDisplay(message)

# Developer
@bot.message_handler(func = lambda message: message.text == DEV_KEY)
def Developer(message):
    ShowDeveloperMode(message)

# Client
@bot.message_handler(func = lambda message: message.text == CLI_KEY)
def ClientMode(message):
    ShowDisplayClientMode(message)

# Settings
@bot.message_handler(func = lambda message: message.text == SETTINGS_KEY)
def ShowSettings(message):
    SettingsDisplay(message)

bot.polling(none_stop = True, interval = 0)