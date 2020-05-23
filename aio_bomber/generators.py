from random import choice
from typing import Dict, Optional

from aio_bomber.constants import LATIN_ALPHABET, LIST_OF_LASTTNAME, LIST_OF_FIRSTNAME


class DynamicDataGenerator:
    def generation(self, dynamic_data: Dict[str, Optional[str]], phone: str) -> Dict[str, str]:
        dynamic_args = {}
        if not dynamic_data:
            raise Exception('Not dynamic_data in json')
        for key, value in dynamic_data.items():
            if key == "formatted_phone":
                dynamic_args[value] = self._formatted_phone(phone)
                continue
            dynamic_args[value] = getattr(self, f"_{key}")()
        return dynamic_args

    @staticmethod
    def _formatted_phone(phone: str) -> str:
        return phone

    @staticmethod
    def _email(mail_url: str = None, len_email: int = 20) -> str:
        mail_url = mail_url or 'gmail.com'
        mail = ''.join([choice(LATIN_ALPHABET) for _ in range(len_email-(len(mail_url) + 1))])
        return f'{mail}@{mail_url}'

    @staticmethod
    def _lastname() -> str:
        return choice(LIST_OF_LASTTNAME)

    @staticmethod
    def _firstname() -> str:
        return choice(LIST_OF_FIRSTNAME)
