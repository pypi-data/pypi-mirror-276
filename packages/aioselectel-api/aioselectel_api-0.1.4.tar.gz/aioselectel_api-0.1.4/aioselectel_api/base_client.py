from abc import ABC, abstractmethod

import aiohttp

from aioselectel_api.config import SELECTEL_STORAGE_BASE_URL
from aioselectel_api.exceptions import SelectelRequestError


class IAuthClient(ABC):  # pylint: disable=too-few-public-methods
    @abstractmethod
    async def authenticate(self, username: str, account_id: str, password: str, project_name: str = None) -> str:
        ...


class BaseClient:
    def __init__(self, keystone_token: str):
        self.keystone_token = keystone_token
        self.base_url = f"{SELECTEL_STORAGE_BASE_URL}"
        self.session = None

    async def __aenter__(self):
        self.session = aiohttp.ClientSession(headers={'X-Auth-Token': self.keystone_token})
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.session.close()

    async def _request(self, method: str, endpoint: str = '', **kwargs):
        """
        Do request to Selectel API
        :param method: PUT, GET, POST, DELETE
        :param endpoint: options, pubdomains
        :param kwargs: data, json, headers
        :return: text or json
        """
        url = f"{self.base_url}/{endpoint}"
        async with self.session.request(method, url, **kwargs) as response:
            if response.status >= 400:
                raise SelectelRequestError(await response.text())
            if response.content_type == 'application/json':
                return await response.json()
            return await response.text()
