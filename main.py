import telebot
import os
from dotenv import load_dotenv
import requests

load_dotenv()
token = os.getenv('AUT_TOKEN')
bot = telebot.TeleBot(token)


def main():
    bot.polling()


@bot.message_handler(commands = ['greet','start'])
def greet(message):
    msg = ''' Hello, how are you? '''
    bot.reply_to(message, msg)


if __name__ == '__main__':
    main()
