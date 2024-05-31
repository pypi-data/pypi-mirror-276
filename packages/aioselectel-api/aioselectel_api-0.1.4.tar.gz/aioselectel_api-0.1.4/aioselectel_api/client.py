import json

import aiohttp

from aioselectel_api.base_client import IAuthClient, BaseClient
from aioselectel_api.exceptions import SelectelRequestError, AuthError


class AuthClient(IAuthClient):  # pylint: disable=too-few-public-methods
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


class SelectelStorageClient(BaseClient):
    def __init__(self, keystone_token: str, container_name: str):
        super().__init__(keystone_token)
        self.base_url += f"/v2/containers/{container_name}"

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

    async def create_logs_task(self, data: dict) -> dict:
        """
        Create a log export task
        param task_type: Type of the log export task
        param container: Name of the container
        param delete_after: Time after which logs should be deleted
        param fields: List of fields to include in the logs
        param filters: Filters to apply to the logs
        param provider: Provider of the logs
        param since: Start time for the logs
        param till: End time for the logs
        :param data: dict of parameters

        Example:
        {
          "data": {
            "container": "string",
            "delete_after": 0,
            "fields": [
              "string"
            ],
            "filters": {
              "additionalProp1": {},
              "additionalProp2": {},
              "additionalProp3": {}
            },
            "provider": "string",
            "since": "2019-05-14T06:00:00",
            "till": "2019-05-14T06:00:00"
          },
          "type": "string"
        }
        """

        try:
            return await self._request('POST', endpoint='logs', data=json.dumps(data))
        except Exception as e:
            raise SelectelRequestError(str(e)) from e

    async def get_logs_task_info(self, task_id: str) -> dict:
        """
        Get information about a log export task
        :param task_id: ID of the log export task
        :return: task details
        """
        try:
            return await self._request('GET', endpoint=f'logs/{task_id}')
        except Exception as e:
            raise SelectelRequestError(str(e)) from e


class SelectelLogsClient(BaseClient):
    def __init__(self, keystone_token: str):
        super().__init__(keystone_token)
        self.base_url += "/v2"

    async def create_logs_task(self, data: dict) -> str:
        """
        Create a log export task
        param task_type: Type of the log export task
        param container: Name of the container
        param delete_after: Time after which logs should be deleted
        param fields: List of fields to include in the logs
        param filters: Filters to apply to the logs
        param provider: Provider of the logs
        param since: Start time for the logs
        param till: End time for the logs
        :param data: dict of parameters
        :return Task id

        Example:
        {
          "data": {
            "container": "string",
            "delete_after": 0,
            "fields": [
              "string"
            ],
            "filters": {
              "additionalProp1": {},
              "additionalProp2": {},
              "additionalProp3": {}
            },
            "provider": "string",
            "since": "2019-05-14T06:00:00",
            "till": "2019-05-14T06:00:00"
          },
          "type": "string"
        }
        """

        try:
            request_data = await self._request('POST', endpoint='logs', data=json.dumps(data))
            return request_data.get('task')['id']
        except Exception as e:
            raise SelectelRequestError(str(e)) from e

    async def get_logs_task_info(self, task_id: str) -> dict:
        """
        Get information about a log export task
        :param task_id: ID of the log export task
        :return: task details
        """
        try:
            return await self._request('GET', endpoint=f'logs/{task_id}')
        except Exception as e:
            raise SelectelRequestError(str(e)) from e


async def get_token(username: str, password: str, account_id: str, project_name) -> str:
    return await AuthClient(
        base_url='https://cloud.api.selcloud.ru'
    ).authenticate(
        username=username, password=password, account_id=account_id, project_name=project_name
    )
