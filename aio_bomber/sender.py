import json
from typing import List, Dict, Any, Union, Optional

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
            try:
                with open(path, 'r', encoding=encoding) as file:
                    services = json.load(file)
            except FileNotFoundError:
                logger.error(f'File not found, path:{path}')
        json_ = await self.get(url=url)
        services.extend(json_)
        return services

    async def get(self, url: str, **kwargs: Union[dict, str]) -> Optional[Dict[str, Any]]:
        return await self.request('get', url=url, **kwargs)

    async def post(self, url: str, data: dict, header: dict = None, **kwargs: Union[dict, str]) -> Optional[Dict[str, Any]]:
        return await self.request('post', url=url, data=data, headers=header, **kwargs)

    async def request(self, method_in_session: str, **kwargs: Union[dict, str]) -> Any:
        try:
            method = getattr(self._session, method_in_session)
            async with method(**kwargs) as response:
                try:
                    json_ = await response.json()
                except client_exceptions.ContentTypeError:
                    json_ = await response.text()
                logger.debug(f'\nFunc args: {kwargs}\nMethod: {method_in_session.upper()}\nResponse: {json_}')
                return json_
        except client_exceptions.TooManyRedirects:
            pass
        except Exception as e:
            logger.exception(e)

    async def close_session(self) -> None:
        await self._session.close()
