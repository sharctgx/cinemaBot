import requests
import json
from bs4 import BeautifulSoup
from requests import get
import urllib
from web_config import *
import random, time
from googlesearch import search


G_URL = 'https://www.google.ru/search'


def get_film_info(query):
    return get_desc(query), get_poster_link(query), get_link(query)


def get_link(query):
    new_query = query + " смотреть онлайн"
    return next(search(new_query, stop=1))


def get_desc(query):
    req = get(G_URL, params = {'q' : query, "gl" : "ru", "hl" : "ru", "lr": "lang_ru"}, headers=header)    
    if (req.status_code != 200):
        raise ConnectionError(req.status_code)
    soup = BeautifulSoup(req.text, "lxml")

    # get description
    try:
        rhs_block = soup.find("div", attrs={"id":"rhs_block"})
        desc_block = rhs_block.find("div", attrs={"class":["kno-rdesc"]})

        description = desc_block.find("span").text
        return description
    except:
        return None


def get_poster_link(query):
    new_query = query + " смотреть онлайн"
    req = get(G_URL, params = {'q' : new_query, 'tbm' : 'isch'}, headers=header)
    if (req.status_code != 200):
        raise ConnectionError(req.status_code)
    soup = BeautifulSoup(req.text, "lxml")

    try:
        search_result = soup.find("div",{"class":"rg_meta"})
        link = json.loads(search_result.text)["ou"]

        return link
    except:
        return None

