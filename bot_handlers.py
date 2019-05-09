import os
import telebot
from telebot import types, apihelper
from megogo_parser import search_films


bot = telebot.TeleBot(os.environ['BOT_TOKEN'])


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Hello, I'm simple echo bot. Tell me something!")


@bot.message_handler(func=lambda m: True)
def echo_all(message):
    response = ""
    for k, v in search_films(message.text).items():
        response = response + k + "\n" + v + "\n"

    bot.reply_to(message, response)


if __name__ == '__main__':
    bot.polling(none_stop=True)
