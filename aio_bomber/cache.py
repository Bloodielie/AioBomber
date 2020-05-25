from abc import ABC, abstractmethod
from typing import Dict, Tuple, Union, Optional, Generator

from aio_bomber.models import ServiceModel


class AbstractCache(ABC):
    @abstractmethod
    def __getitem__(self, item):
        pass

    @abstractmethod
    def __setitem__(self, key, value):
        pass

    @abstractmethod
    def __len__(self):
        pass


class ServicesCache(AbstractCache):
    __slots__ = 'cache'

    def __init__(self) -> None:
        self.cache: Union[dict, Dict[str, Tuple[ServiceModel, dict]]] = {}

    def __getitem__(self, url: str) -> Optional[Tuple[ServiceModel, dict]]:
        return self.cache.get(url)

    def __setitem__(self, key: str, value: Tuple[ServiceModel, dict]) -> None:
        self.cache[key] = value

    def get_dict_values(self) -> Generator[dict, None, None]:
        for value in self.cache.values():
            yield value[1]

    def add_item(self, model: ServiceModel) -> None:
        self.cache[model.url] = (model, model.generator_args())

    def __len__(self) -> int:
        return len(self.cache)
