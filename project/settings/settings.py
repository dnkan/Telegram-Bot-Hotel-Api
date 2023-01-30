"""
Файл содержащий базовые конфигурации бота и API (Токен, API-ключ, заголовок, параметры и url-адреса)
"""

import os
from dotenv import load_dotenv, find_dotenv


if not find_dotenv():
    exit('Файл .env отсутствует')
else:
    load_dotenv()

TOKEN = os.environ.get('TOKEN')
API_KEY = os.environ.get('RAPIDAPI_KEY')

HEADERS = {
    "X-RapidAPI-Key": API_KEY,
    "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
}

URL_SEARCH = 'https://hotels4.p.rapidapi.com/locations/v3/search'
URL_PROPERTY_LIST = 'https://hotels4.p.rapidapi.com/properties/v2/list'
URL_PHOTO = 'https://hotels4.p.rapidapi.com/properties/v2/detail'
URL_HOTEL = 'https://www.hotels.com/ho{}'

QUERY_SEARCH = {
    'q': 'new york',
    'locale': 'en_US',
    'langid': '1033',
    'siteid': '300000001'
}

QUERY_PROPERTY_LIST = {
    'currency': 'USD',
    'eapid': 1,
    'locale': 'en_US',
    'siteId': 300000001,
    'destination': {'regionId': '6054439'},
    'checkInDate': {
        'day': 10,
        'month': 10,
        'year': 2022
    },
    'checkOutDate': {
        'day': 15,
        'month': 10,
        'year': 2022
    },
    'rooms': [
        {
            'adults': 2,
            'children': [{'age': 5}, {'age': 7}]
        }
    ],
    'resultsStartingIndex': 0,
    'resultsSize': 200,
    'sort': 'PRICE_LOW_TO_HIGH',
    'filters': {'price': {
        'max': 150,
        'min': 100
    }}
}

QUERY_BESTDEAL = {
    "currency": "USD",
    "eapid": 1,
    "locale": "en_US",
    "siteId": 300000001,
    "propertyId": "9209612"
}

QUERY_PHOTO = {
    "currency": "USD",
    "eapid": 1,
    "locale": "en_US",
    "siteId": 300000001,
    "propertyId": "9209612"
}
