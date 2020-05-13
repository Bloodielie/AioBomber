from typing import Dict, Optional
from random import choice
from loguru import logger
import sys


def configuration_logger(error_handler: bool = False) -> None:
    logger.remove()
    logger.add(sys.stdout, colorize=True, format="<green>{time:YYYY-MM-DD at HH:mm:ss}</green> | <level>{level}</level> | {message}",
               level="INFO")
    if error_handler:
        logger.add('error.log', format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}",
                   level="ERROR")


class BomberUtils:
    @staticmethod
    def generate_email(mail_url: str = None, len_email: int = 10) -> str:
        mail_url = mail_url or 'gmail.com'
        lat_alf = 'abcdefghijklmnopqrstuvwxyz'
        mail = ''.join([choice(lat_alf) for _ in range(len_email)])
        return f'{mail}@{mail_url}'

    def generate_args(self, service: dict, phone: str) -> Dict[str, Optional[str]]:
        args = {}
        url = service.get('url')
        if not url:
            raise Exception('Not url in json')
        args['url'] = url
        static_data = service.get('static_data')
        if static_data:
            args['data'] = static_data
        else:
            args['data'] = {}

        data_args = args.copy()['data']
        dynamic_data = service.get('dynamic_data')
        if not dynamic_data:
            raise Exception('Not dynamic_data in json')
        if dynamic_data.get('email'):
            data_args['email'] = self.generate_email()
        formatted_phone = dynamic_data.get('formatted_phone')
        if formatted_phone:
            data_args[formatted_phone] = phone
        else:
            raise Exception('Not phone in json')
        args.update({'data': data_args})

        return args
