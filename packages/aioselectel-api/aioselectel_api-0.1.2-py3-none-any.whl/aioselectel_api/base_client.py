from abc import ABC, abstractmethod


class IClient(ABC):  # pylint: disable=too-few-public-methods
    @abstractmethod
    async def authenticate(self, username: str, account_id: str, password: str, project_name: str = None) -> str:
        ...
