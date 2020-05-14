from loguru import logger
import sys
from random import choice
from .constants import LATIN_ALPHABET, LIST_OF_FIRSTNAME, LIST_OF_LASTTNAME


def configuration_logger(error_handler: bool = False, is_debug: bool = False) -> None:
    logger.remove()
    if is_debug:
        level = 'DEBUG'
    else:
        level = 'INFO'
    logger.add(sys.stdout, colorize=True, format="<green>{time:YYYY-MM-DD at HH:mm:ss}</green> | <level>{level}</level> | {message}",
               level=level)
    if error_handler:
        logger.add('error.log', format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}",
                   level="ERROR")


class LineGenerator:
    @staticmethod
    def generate_email(mail_url: str = None, len_email: int = 10) -> str:
        mail_url = mail_url or 'gmail.com'
        mail = ''.join([choice(LATIN_ALPHABET) for _ in range(len_email)])
        return f'{mail}@{mail_url}'

    @staticmethod
    def generate_firstname():
        return choice(LIST_OF_FIRSTNAME)

    @staticmethod
    def generate_lastname():
        return choice(LIST_OF_LASTTNAME)
