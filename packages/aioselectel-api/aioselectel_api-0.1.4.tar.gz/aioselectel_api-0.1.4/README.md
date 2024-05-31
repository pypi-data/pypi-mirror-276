# Selectel async API

[![Pylint](https://github.com/azamtoiri/aioselectel_api/actions/workflows/pylint.yml/badge.svg)](https://github.com/azamtoiri/aioselectel_api/actions/workflows/pylint.yml) [![Upload Python Package](https://github.com/azamtoiri/aioselectel_api/actions/workflows/python-publish-with-pip.yml/badge.svg)](https://github.com/azamtoiri/aioselectel_api/actions/workflows/python-publish-with-pip.yml)

# Version 0.1.4

# logs creating
* Created new class `SelectelLogsClient` for logs
* Create Base Class for Client and separated clases

### SelectelLogsClient
* have to functions - `get_logs_task_info` and `create_logs_task`

### Using of this class
```python
    async with SelectelLogsClient(keystone_token=keystone_token) as client:
        task = {  # task with parameters
            "data": {
                "container": "links",
                "delete_after": 0,
                # "fields": [
                #     ""
                # ],
                # "filters": {
                #     "additionalProp1": {},
                #     "additionalProp2": {},
                #     "additionalProp3": {}
                # },
                # "provider": "",
                "since": "2024-05-30T06:00:00",
                "till": "2024-05-30T06:00:00"
            },
            # "type": ""

        }
        task_id = await client.create_logs_task(task)
        await client.get_logs_task_info(task_id)
```
Use like 

## Simple using

```python
import asyncio

from environs import Env

from aioselectel_api.client import SelectelStorageClient, get_token

env = Env()
env.read_env('.env')

username = env('SELECTEL_USERNAME')
password = env('SELECTEL_PASSWORD')
account_id = env('SELECTEL_ACCOUNT_ID')

"""
USING ONLY Selectel Storage API 😑
"""


async def main():
    keystone_token = await get_token(username=username, password=password, account_id=account_id,
                                     project_name='My First Project')
    async with SelectelStorageClient(keystone_token=keystone_token, container_name='links') as client:
        print(await client.get_pubdomains())
        print(await client.get_containers_settings())


if __name__ == '__main__':
    asyncio.run(main())

```
