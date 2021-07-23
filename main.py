import telebot
import os
from dotenv import load_dotenv
import requests

load_dotenv()
token = os.getenv('AUT_TOKEN')
bot = telebot.TeleBot(token)

@bot.message_handler(commands = ['greet','start'])
def greet(message):
    msg = ''' C4X IS THE WORST'''
    bot.reply_to(message, msg)


def main():
    bot.polling(none_stop=False, interval=0, timeout=20)


if __name__ == '__main__':
    main()
