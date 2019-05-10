import os
import telebot
from telebot import types, apihelper
import megogo_parser 


bot = telebot.TeleBot(os.environ['BOT_TOKEN'])


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Hello, I'm simple cinema bot in development!")


@bot.message_handler(commands=['find']) 
def find(message):
	bot.send_message(message.chat.id, 'Введите название фильма')
	bot.register_next_step_handler(message, search_film)


def search_film(message):
    response = megogo_parser.search_films(message.text)
    
    if response:
        keyboard = types.InlineKeyboardMarkup()

        buttons = [types.InlineKeyboardButton(text=k, callback_data=v)\
            for k, v in response.items()]

        keyboard.add(*buttons)

        bot.send_message(message.chat.id, 'Вот что нашёл:', reply_markup=keyboard)
        bot.reply_to(message, response)
    else:
        bot.reply_to(message, "Я не нашёл этот фильм.\
             Возможно, вы найдёте то, что искали, после следующего обновления бота")


if __name__ == '__main__':
    bot.polling(none_stop=True)
