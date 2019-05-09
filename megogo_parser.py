import requests
import json
from bs4 import BeautifulSoup
from requests import get
import urllib

class_section = "widget searchVideoCatalog_v1 product-main"
class_div = "card videoItem direction-vertical orientation-portrait size-normal type-normal"
class_div_content = "card-content video-content"

def search_films(query):
    """
    Searches for films. Returns dict {text : link}
    """
    url = f'https://megogo.ru/ru/search-extended?q={query}&tab=video'
    req = get(url)
    print("url:", url, "\n")
    
    soup = BeautifulSoup(req.text, "lxml")

    result = {}

    try:
        section = \
            soup.find('section', attrs={'class' : class_section})

        for film_preview in section.findAll('div', attrs={'class' : class_div}):
            content = film_preview.find('div', attrs={'class' : class_div_content})
            link = content.find('a')
            result[link.find('h3').text.strip(" \n")] = 'https://megogo.ru' + link['href']

    except AttributeError:
        print(req.text)
        
    return result
