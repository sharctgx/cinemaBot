from vedis import Vedis
import os
from enum import Enum
import json


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
            return False


def add_current_search_results(user_id, results_dict):
    results_json = json.dumps(results_dict)

    with Vedis(os.environ['DB_FILENAME']) as db:
        try:
            db[str(user_id) + "res"] = results_json
            return True
        except:
            return False


def get_result(user_id, idx):
    with Vedis(os.environ['DB_FILENAME']) as db:
        try:
            results_list = json.loads(db[str(user_id) + "res"].decode())
            return results_list[idx]
        except (KeyError, IndexError):  # Если такого ключа почему-то не оказалось или idx вышел за пределы
            return (None, None)


def get_response(user_id):
    with Vedis(os.environ['DB_FILENAME']) as db:
        try:
            return json.loads(db[str(user_id) + "res"].decode())
        except KeyError:
            return None

def cache_query(user_id, query):
    with Vedis(os.environ['DB_FILENAME']) as db:
        try:
            db[str(user_id) + "query"] = query
            return True
        except:
            return False


def get_last_query(user_id):
    with Vedis(os.environ['DB_FILENAME']) as db:
        try:
            return db[str(user_id)  + "query"].decode()
        except (KeyError, IndexError):
            return None
