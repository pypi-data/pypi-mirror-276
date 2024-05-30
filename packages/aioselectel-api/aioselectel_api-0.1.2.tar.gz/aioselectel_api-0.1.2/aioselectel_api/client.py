import json

import aiohttp

from aioselectel_api.config import SELECTEL_STORAGE_BASE_URL
from aioselectel_api.base_client import IClient
from aioselectel_api.exceptions import SelectelRequestError, AuthError


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

    async def get_containers_settings(self) -> dict:
        return await self._request('GET', endpoint='options')

    async def get_pubdomains(self) -> dict:
        return await self._request('GET', endpoint='pubdomains')

    async def set_containers_options(self, data: dict) -> bool:
        """
        Set metadata for container
        :param metadata: dict
        :return: True or false
        """
        # payload = {
        #     "general": {
        #         "cache_control": "max-age=604800", # 1 week
        #         "default_delete_after": 3600, # 1 hour
        #         "type": "private" # public, private
        #     },
        #     "quota": {
        #         "max_bytes_used": 1024, # 1 KB
        #         "max_object_count": 10, # 10 objects
        #     },
        #     "web": {
        #         "error": "error.html", # error.html
        #         "expires": "Wed, 21 Oct 2015 07:28:00 GMT", # Wed, 21 Oct 2015 07:28:00 GMT
        #         "index": "index.html", # index.html
        #         "listing_css": "style.css", # style.css
        #         "listing_enabled": True, # true
        #         "listing_sort_order": "name_asc" # name_asc, name_desc, size_asc, size_desc, time_asc, time_desc
        #     }
        # }
        try:
            return await self._request('PUT', endpoint='options', data=json.dumps(data))
        except Exception as e:
            raise SelectelRequestError(str(e)) from e


async def get_token(username: str, password: str, account_id: str, project_name) -> str:
    return await AuthClient(
        base_url='https://cloud.api.selcloud.ru'
    ).authenticate(
        username=username, password=password, account_id=account_id, project_name=project_name
    )
