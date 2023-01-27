"""
Файл для создания экземпляров: бота и логгера.
Так же содержит декоратор для отлова исключений и логгирования ошибок
"""
from typing import Callable

from requests import ReadTimeout
from telebot import TeleBot
from project.database.models import user
from project.logging_config import custom_logger
from project.settings import constants
from project.settings.settings import TOKEN

logger = custom_logger('bot_logger')
bot = TeleBot(token=TOKEN)


def exception_handler(func: Callable) -> Callable:
    """
    Декоратор - оборачивающий функцию в try-except блок.

    :param func: Callable
    :return: Callable
    """
    def wrapped_func(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            return result
        except Exception as error:
            logger.error('В работе бота возникло исключение', exc_info=error)
            bot.send_message(user.user.user_id, constants.REQUEST_ERROR)
    return wrapped_func


def exception_request_handler(func: Callable) -> Callable:
    """
    Декоратор - оборачивающий функцию request в try-except блок.

    :param func: Callable
    :return: Callable
    """
    def wrapped_func(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            return result
        except (ConnectionError, TimeoutError, ReadTimeout) as error:
            logger.error('В работе бота возникло исключение', exc_info=error)
            bot.send_message(user.user.user_id, constants.REQUEST_ERROR)
    return wrapped_func
