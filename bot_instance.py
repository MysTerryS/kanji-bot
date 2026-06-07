import telebot
from dotenv import load_dotenv
from os import getenv

load_dotenv()
token = getenv("token")
bot = telebot.TeleBot(token = token)