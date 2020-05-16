from typing import Dict, Any
from loguru import logger
from aiohttp import ClientSession, client_exceptions
try:
    import ujson as json
except ImportError:
    import json


class Sender:
    _headers = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 5.0.2; 7045Y Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2728.43 Mobile Safari/537.36",
        "X-Requested-With": "XMLHttpRequest",
    }

    def __init__(self, session: ClientSession = None):
        self._session = session or ClientSession(json_serialize=json.dumps)

    async def get_services(self, path: str, encoding: str = 'utf-8') -> Dict[str, Any]:
        with open(path, 'r', encoding=encoding) as file:
            return json.load(file)

    async def post(self, url: str, data: dict, header: dict = None) -> Dict[str, Any]:
        if not header:
            header = self._headers
        else:
            header.update(self._headers)
        try:
            async with self._session.post(url=url, data=data, headers=header) as response:
                try:
                    json_ = await response.json()
                except client_exceptions.ContentTypeError:
                    json_ = await response.text()
                logger.debug(f'{url}\n{json_}\n')
                return json_
        except Exception as e:
            logger.error(e)

    async def close_session(self) -> None:
        await self._session.close()
