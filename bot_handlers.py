import os
import telebot
from telebot import types, apihelper
import megogo_parser 
import dbworker
from dbworker import States


bot = telebot.TeleBot(os.environ['BOT_TOKEN'])


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Hello, I'm a simple cinema bot in development!")


@bot.message_handler(commands=['find']) 
def find(message):
    bot.send_message(message.chat.id, 'Введите название фильма')
    dbworker.set_state(message.chat.id, States.S_ENTER_NAME.value)


@bot.message_handler(commands=['reset'])
def reset(message):
    bot.send_message(message.chat.id, 'Выход из текущего поиска')
    dbworker.set_state(message.chat.id, States.S_START.value)  


@bot.message_handler(func=lambda message:
     dbworker.get_current_state(message.chat.id) == States.S_ENTER_NAME.value)
def search_film(message):
    response = megogo_parser.search_films(message.text)
    
    if response:
        print(response)
        dbworker.add_current_search_results(message.chat.id, response)

        keyboard = types.InlineKeyboardMarkup()

        for idx, film_info in enumerate(response):
            keyboard.add(types.InlineKeyboardButton(text=film_info[0], callback_data="url:" + idx))

        bot.reply_to(message, 'Вот что я нашёл:', reply_markup=keyboard)
    else:
        print("No response")
        
        bot.reply_to(message, "Я не нашёл этот фильм.\
             Возможно, вы найдёте то, что искали, после следующего обновления бота")


@bot.callback_query_handler(func=lambda call: call.data[:4] == "url:")
def choose_option(call):
    idx = call.data[4:]
    film_info = dbworker.get_result(call.message.chat.id, idx)

    show_film_info(film_info[1], chat_id = call.message.chat.id, message_id = call.message.message_id)
    dbworker.set_state(call.message.chat.id, States.S_EVALUATE_OPTION.value)


def show_film_info(url, chat_id, message_id):
    description, poster, link = megogo_parser.get_film_info(url)
    # change message
    film_preview_keyboard = types.InlineKeyboardMarkup()
    film_preview_keyboard.add(types.InlineKeyboardButton(text="Смотреть!", url=link))

    film_preview_text = f"{description}\n\n{poster}"
    
    bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=film_preview_text,
     reply_markup=film_preview_keyboard)


if __name__ == '__main__':
    bot.polling(none_stop=True)
