import requests
import json
from bs4 import BeautifulSoup
from requests import get
import urllib

proxy_dict = {'https':'socks5://91.105.233.236:1080'}

class_section = "widget searchVideoCatalog_v1 product-main "
class_div = "card videoItem direction-vertical orientation-portrait size-normal type-normal"
class_div_content = "card-content video-content"

def search_films(query):
    """
    Searches for films. Returns dict {text : link}
    """
    url = f'https://megogo.ru/ru/search-extended?q={query}'
    req = get(url, proxies=proxy_dict)
    
    soup = BeautifulSoup(req.text, "lxml")

    result = {}

    try:
        section = \
            soup.find('section', attrs={'class' : class_section})

        for film_preview in section.findAll('div', attrs={'class' : class_div}):
            print("film_preview: ", film_preview, "\n\n")
            content = film_preview.find('div', attrs={'class' : class_div_content})
            print("content: ", content, "\n\n")
            link = content.find('a')
            result[link.find('h3').text.strip(" \n")] = 'https://megogo.ru' + link['href']

    except AttributeError:
        print(section.findAll('div', attrs={'class' : class_div}))
        
    return result
