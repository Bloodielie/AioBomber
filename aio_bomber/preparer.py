from typing import Dict, Union

from .generators import DynamicDataGenerator
from .models import ServiceModel


class InformationPreparer:
    def __init__(self):
        self.cache = []
        self.dynamic_data_generator = DynamicDataGenerator()

    def get_json_model(self, service: Dict[str, Union[str, dict]], phone: str) -> ServiceModel:
        dynamic_data = service.get('dynamic_data')
        service.update({'dynamic_data': self.dynamic_data_generator.generation(dynamic_data, phone)})
        json_data = ServiceModel(**service)
        self.cache.append(json_data)
        return json_data

    def __len__(self) -> int:
        return len(self.cache)
