import os
import telebot
from telebot import types, apihelper
import megogo_parser 
import google_parser
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
    dbworker.set_state(message.chat.id, States.S_CHOOSE_OPTION.value)

    if response:
        print(response)
        dbworker.add_current_search_results(message.chat.id, response)

        keyboard = types.InlineKeyboardMarkup()

        for idx, film_info in enumerate(response):
            keyboard.add(types.InlineKeyboardButton(text=film_info[0], callback_data="url:" + str(idx)))

        bot.reply_to(message, 'Вот что я нашёл:', reply_markup=keyboard)
    else:
        print("No response")
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(types.InlineKeyboardButton(text="Мне повезёт!", callback_data="google"))

        
        bot.reply_to(message, "В моих онлайн-сервисах нет этого фильма :(\n\
            Могу попробовать загуглить его для вас.")


@bot.callback_query_handler(func=lambda call: call.data == "google")
def google_film(call):
    query = dbworker.get_last_query(call.message.chat.id)
    if (query):
        show_film_info(query, chat_id = call.message.chat.id, message_id = call.message.message_id,
            parser = google_parser)


@bot.callback_query_handler(func=lambda call: call.data[:4] == "url:")
def choose_option(call):
    idx = int(call.data[4:])
    film_info = dbworker.get_result(call.message.chat.id, idx)

    show_film_info(film_info[1], chat_id = call.message.chat.id, message_id = call.message.message_id,
        parser = megogo_parser)
    dbworker.set_state(call.message.chat.id, States.S_EVALUATE_OPTION.value)


def show_film_info(url_or_query, chat_id, message_id, parser):
    description, poster, link = parser.get_film_info(url_or_query)
    # change message
    film_preview_keyboard = types.InlineKeyboardMarkup()
    film_preview_keyboard.add(types.InlineKeyboardButton(text="Смотреть!", url=link))

    film_preview_text = f"{description}\n\n{poster}"
    
    bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=film_preview_text,
     reply_markup=film_preview_keyboard)


if __name__ == '__main__':
    bot.polling(none_stop=True)
