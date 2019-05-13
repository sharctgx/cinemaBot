from vedis import Vedis
import os
from enum import Enum


class States(Enum):
    """
    Мы используем БД Vedis, в которой хранимые значения всегда строки,
    поэтому и тут будем использовать тоже строки (str)
    """
    S_START = "0" 
    S_ENTER_NAME = "1"
    S_CHOOSE_OPTION = "2"
    S_EVALUATE_OPTION = "3"

# Пытаемся узнать из базы «состояние» пользователя
def get_current_state(user_id):
    with Vedis(os.environ['DB_FILENAME']) as db:
        try:
            return db[user_id].decode()
        except KeyError:  # Если такого ключа почему-то не оказалось
            db[user_id] = States.S_START.value
            return db[user_id].decode()  # значение по умолчанию - начало диалога

# Сохраняем текущее «состояние» пользователя в нашу базу
def set_state(user_id, value):
    with Vedis(os.environ['DB_FILENAME']) as db:
        try:
            db[user_id] = value
            return True
        except:
            # тут желательно как-то обработать ситуацию
            return False
