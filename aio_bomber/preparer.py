from typing import Dict, Union, Tuple

from .generators import DynamicDataGenerator
from .models import ServiceModel


class InformationPreparer:
    def __init__(self):
        self.cache: Union[dict, Dict[str, Tuple[ServiceModel, dict]]] = {}
        self.dynamic_data_generator = DynamicDataGenerator()

    def get_service_model(self,
                          service: Dict[str, Union[str, dict]],
                          phone: str,
                          is_save_in_cache: bool = True) -> ServiceModel:
        dynamic_data = service.get('dynamic_data')
        service.update({'dynamic_data': self.dynamic_data_generator.generation(dynamic_data, phone)})
        service_model = ServiceModel(**service)
        if is_save_in_cache:
            self.set_data_in_cache(service_model)
        return service_model

    def set_data_in_cache(self, service_model: ServiceModel) -> None:
        self.cache[service_model.url] = (service_model, service_model.generator_args())

    def __len__(self) -> int:
        return len(self.cache)
