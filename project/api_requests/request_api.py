import requests
import string

from requests import Response
from telebot.types import Message, CallbackQuery
from project.loader import logger, exception_request_handler
from project.settings import constants
from project.settings.settings import QUERY_SEARCH, URL_SEARCH, HEADERS, QUERY_PROPERTY_LIST, URL_PROPERTY_LIST, QUERY_BESTDEAL

from project.database.models import user


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
    QUERY_SEARCH['currency'] = user.user.currency
    QUERY_SEARCH['langid'] = user.user.langid
    QUERY_SEARCH['siteid'] = user.user.siteid
    QUERY_SEARCH['q'] = message.text
    user.edit('locale', QUERY_SEARCH['locale'])
    response = requests.request('GET', URL_SEARCH, headers=HEADERS, params=QUERY_SEARCH, timeout=15)
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
    QUERY_PROPERTY_LIST['regionId'] = user.user.city_id
    QUERY_PROPERTY_LIST['eapid'] = user.user.eapid
    QUERY_PROPERTY_LIST['checkInDate'] = {
		user.user.day,
		user.user.month,
		user.user.year
	}
    QUERY_PROPERTY_LIST['checkOutDate'] = {
		user.user.day,
		user.user.month,
		user.user.year
	}
    QUERY_PROPERTY_LIST['rooms'] = {
        user.user.adults,
        user.user.children
    }
    QUERY_PROPERTY_LIST['currency'] = user.user.currency
    QUERY_PROPERTY_LIST['locale'] = user.user.locale
    QUERY_PROPERTY_LIST['filters'] = {
        user.user.max,
        user.user.min
    }
    response = requests.request('POST', URL_PROPERTY_LIST, headers=HEADERS, params=QUERY_PROPERTY_LIST, timeout=15)
    return response


@exception_request_handler
def request_bestdeal(call: CallbackQuery) -> Response:
    """
    Функция - делающая запрос на API по адресу: 'https://hotels4.p.rapidapi.com/properties/v2/detail'. Предназначена для
    команды bestdeal. Исключительность данной функции под функционал одной команды заключается в широкой
    установке параметров для поиска. Возвращает Response, содержащий в себе список отелей в выбранном городе.

    :param call: CallbackQuery
    :return: Response
    """
    logger.info(str(call.from_user.id))
    QUERY_BESTDEAL['siteId'] = user.user.city_id
    QUERY_BESTDEAL['eapid'] = user.user.eapid
    QUERY_BESTDEAL['propertyId'] = user.user.propertyId
    QUERY_BESTDEAL['currency'] = user.user.currency
    QUERY_BESTDEAL['locale'] = user.user.locale
    response = requests.request('POST', URL_PROPERTY_LIST, headers=HEADERS, params=QUERY_BESTDEAL, timeout=15)
    return response


