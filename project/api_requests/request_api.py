import requests
import string

from requests import Response
from telebot.types import Message, CallbackQuery
from loader import logger, exception_request_handler
from settings import constants
from settings.settings import QUERY_SEARCH, URL_SEARCH, HEADERS, QUERY_PROPERTY_LIST, URL_PROPERTY_LIST, \
    QUERY_PHOTO, URL_PHOTO
from database.models import user


@exception_request_handler
def request_search(message: Message) -> Response:
    """
    Функция - делающая запрос на API по адресу: 'https://hotels4.p.rapidapi.com/locations/v3/search'
    Проверяет введённые пользователем символы на ASCII кодировку, если так, то ищет с параметром locale en_US,
    в противном случае ищет с парметром locale ru_RU. Возвращает Response, содержащий в себе список городов.

    :param message: Message
    :return: Response
    """
    logger.info(str(message.from_user.id))
    for sym in message.text:
        if sym not in string.printable:
            QUERY_SEARCH['locale'] = 'ru_RU'
            break
    QUERY_SEARCH['q'] = message.text
    response = requests.get(URL_SEARCH, headers=HEADERS, params=QUERY_SEARCH)
    return response


@exception_request_handler
def request_property_list(call: CallbackQuery) -> Response:
    """
    Функция - делающая запрос на API по адресу: 'https://hotels4.p.rapidapi.com/properties/v2/list'
    Предназначена для команд lowprice и highprice. В зависимости от введенной команды сортирует ответ
    по возврастанию цены, или же по убыванию. Возвращает Response, содержащий в себе список отелей в выбранном городе.

    :param call: CallbackQuery
    :return: Response
    """
    logger.info(str(call.from_user.id))
    if user.user.command == constants.HIGHPRICE[1:]:
        QUERY_PROPERTY_LIST['sort'] = '-PRICE_LOW_TO_HIGH'
    QUERY_PROPERTY_LIST['currency'] = user.user.currency
    QUERY_PROPERTY_LIST['destination'] = {'regionId': user.user.city_id}
    QUERY_PROPERTY_LIST['checkInDate'] = {'day': int(user.user.date_in.split('-')[2]),
                                          'month': int(user.user.date_in.split('-')[1]),
                                          'year': int(user.user.date_in.split('-')[0])}
    QUERY_PROPERTY_LIST['checkOutDate'] = {'day': int(user.user.date_out.split('-')[2]),
                                           'month': int(user.user.date_out.split('-')[1]),
                                           'year': int(user.user.date_out.split('-')[0])}
    response = requests.post(URL_PROPERTY_LIST, json=QUERY_PROPERTY_LIST, headers=HEADERS, timeout=15)
    return response


@exception_request_handler
def request_bestdeal_list(call: CallbackQuery) -> Response:
    """
    Функция - делающая запрос на API по адресу: 'https://hotels4.p.rapidapi.com/properties/v2/list'
    Предназначена для команд lowprice и highprice. В зависимости от введенной команды сортирует ответ
    по возврастанию цены, или же по убыванию. Возвращает Response, содержащий в себе список отелей в выбранном городе.

    :param call: CallbackQuery
    :return: Response
    """
    logger.info(str(call.from_user.id))
    if user.user.command == constants.HIGHPRICE[1:]:
        QUERY_PROPERTY_LIST['sort'] = '-PRICE_LOW_TO_HIGH'
    QUERY_PROPERTY_LIST['currency'] = user.user.currency
    QUERY_PROPERTY_LIST['destination'] = {'regionId': user.user.city_id}
    QUERY_PROPERTY_LIST['checkInDate'] = {'day': int(user.user.date_in.split('-')[2]),
                                          'month': int(user.user.date_in.split('-')[1]),
                                          'year': int(user.user.date_in.split('-')[0])}
    QUERY_PROPERTY_LIST['checkOutDate'] = {'day': int(user.user.date_out.split('-')[2]),
                                           'month': int(user.user.date_out.split('-')[1]),
                                           'year': int(user.user.date_out.split('-')[0])}
    QUERY_PROPERTY_LIST['filters']['price'] = {'max': user.user.price_max,
                                               'min': user.user.price_min}
    response = requests.post(URL_PROPERTY_LIST, json=QUERY_PROPERTY_LIST, headers=HEADERS, timeout=15)
    return response


@exception_request_handler
def request_photo(call: CallbackQuery, id_hotel) -> Response:
    """
    Функция - делающая запрос на API по адресу: 'https://hotels4.p.rapidapi.com/properties/v2/detail'. Предназначена для
    команды bestdeal. Исключительность данной функции под функционал одной команды заключается в широкой
    установке параметров для поиска. Возвращает Response, содержащий в себе список отелей в выбранном городе.

    :param call: CallbackQuery
    :return: Response
    """
    logger.info(str(call.from_user.id))
    QUERY_PHOTO['propertyId'] = id_hotel
    response = requests.post(URL_PHOTO, json=QUERY_PHOTO, headers=HEADERS, timeout=15)
    return response
