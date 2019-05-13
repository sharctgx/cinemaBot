import requests
import json
from bs4 import BeautifulSoup
from requests import get
import urllib
from web_config import *


# нужные тэги для парсинга (хорошо бы вынести в отдельный конфиг)
class_section = ['widget', 'searchExtended_v1', 'product-main']
class_div = ['card', 'videoItem', 'direction-vertical', 'orientation-portrait',
             'size-normal', 'type-normal']
class_div_content = ['card-content', 'video-content']
class_div_content_film_page = ["videoView-content"]


def search_films(query, limit = 5):
    """
    Searches for films. Returns dict {text : link}.
    """
    url = f'https://megogo.ru/ru/search-extended?q={query}&tab=video'
    req = get(url, proxies=proxy_dict, headers=header)
    
    soup = BeautifulSoup(req.text, "lxml")

    result = {}
    n_added = 0

    try:
        section = \
            soup.find('section', attrs={'class' : class_section})

        for film_preview in section.findAll('div', attrs={'class' : class_div}):
            content = film_preview.find('div', attrs={'class' : class_div_content})
            link = content.find('a')
            result[link.find('h3').text.strip(" \n")] = 'https://megogo.ru' + link['href']
            n_added += 1
            if (n_added >= limit):
                break

    except AttributeError:
        for s in soup.findAll('section'):
            print(s['class'])
        
    return result


def get_film_info(url):
    """
    Parses film page at url and returns film description, poster and link to watch online.
    """
    req = get(url, proxies=proxy_dict, headers=header)
    soup = BeautifulSoup(req.text, "lxml")

    content = soup.find("div", attrs={'class' : class_div_content_film_page})

    description = content.find("div", attrs = {"class" : "show-more"}).text
    poster_url = content.find("div", attrs = {"class" : "thumb"}).find('img')['src']

    # img_data = get(poster_url, proxies=proxy_dict, headers=header).content

    return description, poster_url, url

