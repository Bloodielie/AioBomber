from typing import Dict, Optional
from .utils import LineGenerator


class Preparer:
    def __init__(self):
        self._line_generator = LineGenerator()

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
            data_args['email'] = self._line_generator.generate_email()
        lastname = dynamic_data.get('lastname')
        if lastname:
            data_args[lastname] = self._line_generator.generate_lastname()
        firstname = dynamic_data.get('firstname')
        if firstname:
            data_args[firstname] = self._line_generator.generate_firstname()

        formatted_phone = dynamic_data.get('formatted_phone')
        if formatted_phone:
            data_args[formatted_phone] = phone
        else:
            raise Exception('Not phone in json')
        args.update({'data': data_args})
        return args
