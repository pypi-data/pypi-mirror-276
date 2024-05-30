import aiohttp


class ClientCreatorContext:
    def __init__(self, coro):
        self._coro = coro
        self._client = None

    async def __aenter__(self):
        self._client = await self._coro
        return await self._client.__aenter__()

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self._client.__aexit__(exc_type, exc_val, exc_tb)


class SelectelSession:
    def __init__(self, base_url):
        self.base_url = base_url
        self.session = aiohttp.ClientSession()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.session.close()

    async def request(self, method, path, **kwargs):
        url = f"{self.base_url}{path}"
        async with self.session.request(method, url, **kwargs) as response:
            return response

    async def get(self, path, **kwargs):
        return await self.request("GET", path, **kwargs)

    async def post(self, path, **kwargs):
        return await self.request("POST", path, **kwargs)

    async def put(self, path, **kwargs):
        return await self.request("PUT", path, **kwargs)

    async def delete(self, path, **kwargs):
        return await self.request("DELETE", path, **kwargs)
