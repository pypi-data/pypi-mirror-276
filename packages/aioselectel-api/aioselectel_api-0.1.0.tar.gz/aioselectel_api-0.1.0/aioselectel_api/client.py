import json

import aiohttp

from aioselectel_api.config import SELECTEL_STORAGE_BASE_URL
from .base_client import IClient
from .exceptions import SelectelRequestError, AuthError


class AuthClient(IClient):  # pylint: disable=too-few-public-methods
    def __init__(self, base_url: str):
        self.token = None
        self.base_url = base_url

    async def authenticate(self, username: str, account_id: str, password: str, project_name: str = None) -> str:
        """
        Create Keystone Token
        if project name create for project
        :param username: str username of Service user
        :param account_id: str your account id On right side of the corner
        :param password: str password of Service user
        :param project_name: your project name
        :return: str [KEYSTONE TOKEN]
        """
        url = f'{self.base_url}/identity/v3/auth/tokens'
        headers = {'Content-Type': 'application/json'}
        payload = {
            "auth": {
                "identity": {
                    "methods": ["password"],
                    "password": {
                        "user": {
                            "name": username,
                            "domain": {"name": account_id},
                            "password": password
                        }
                    }
                },
                "scope": {
                    "domain": {"name": account_id}
                }
            }
        }
        if project_name:
            payload['auth']['scope'].pop('domain', None)
            payload['auth']['scope']['project'] = {"name": project_name, "domain": {"name": account_id}}
        else:
            # Если не передано имя проекта, удаляем блок с проектом из payload
            payload['auth']['scope'].pop('project', None)

        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, data=json.dumps(payload)) as response:
                if response.status != 201:
                    raise AuthError(f"Authentication failed with status {response.status}")
                self.token = response.headers.get('X-Subject-Token')
                return self.token


class SelectelStorageClient:
    def __init__(self, keystone_token: str, container_name: str):
        self.keystone_token = keystone_token
        self.container_name = container_name
        self.base_url = f"{SELECTEL_STORAGE_BASE_URL}/v2/containers/{container_name}"
        self.session = None

    async def __aenter__(self):
        self.session = aiohttp.ClientSession(headers={'X-Auth-Token': self.keystone_token})
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.session.close()

    async def _request(self, method: str, endpoint: str = '', **kwargs):
        url = f"{self.base_url}/{endpoint}"
        async with self.session.request(method, url, **kwargs) as response:
            if response.status >= 400:
                raise SelectelRequestError(await response.text())
            if response.content_type == 'application/json':
                return await response.json()
            return await response.text()

    async def get_containers_settings(self):
        return await self._request('GET', endpoint='options')

    async def get_pubdomains(self):
        return await self._request('GET', endpoint='pubdomains')

    async def set_account_metadata(self, metadata: dict):
        headers = {f'X-Account-Meta-{k}': v for k, v in metadata.items()}
        return await self._request('POST', headers=headers)


async def get_token(username: str, password: str, account_id: str, project_name) -> str:
    return await AuthClient(
        base_url='https://cloud.api.selcloud.ru'
    ).authenticate(
        username=username, password=password, account_id=account_id, project_name=project_name
    )
