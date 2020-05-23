import json
from typing import List, Dict, Any

from aiohttp import ClientSession, client_exceptions
from loguru import logger
from .constants import API_LINK


class Sender:
    _headers = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 5.0.2; 7045Y Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2728.43 Mobile Safari/537.36",
        "X-Requested-With": "XMLHttpRequest",
    }

    def __init__(self, session: ClientSession = None):
        self._session = session or ClientSession(headers=self._headers)

    async def get_services(self, path: str = None, url: str = None, encoding: str = 'utf-8') -> List[Dict[str, Any]]:
        url = url if url is not None else API_LINK
        services = []
        if path is not None:
            with open(path, 'r', encoding=encoding) as file:
                services = json.load(file)
        async with self._session.get(url=url) as response:
            json_ = await response.json()
            services.extend(json_)
        return services

    async def post(self, url: str, data: dict, header: dict = None) -> Dict[str, Any]:
        try:
            async with self._session.post(url=url, data=data, headers=header) as response:
                try:
                    json_ = await response.json()
                except client_exceptions.ContentTypeError:
                    json_ = await response.text()
                logger.debug(f'{url}\n{json_}\n')
                return json_
        except client_exceptions.TooManyRedirects:
            pass
        except Exception as e:
            logger.exception(e)

    async def close_session(self) -> None:
        await self._session.close()
