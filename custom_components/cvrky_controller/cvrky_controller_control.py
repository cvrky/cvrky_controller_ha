import aiohttp
import json


async def _request(host, path, username, password):
    auth = aiohttp.BasicAuth(username, password)
    async with aiohttp.ClientSession() as session:
        async with session.get(f"http://{host}{path}", auth=auth) as resp:
            if resp.status != 200:
                raise ValueError(f"Request failed with {resp.status}/{resp.reason}")
            return await resp.text()


class CvrkyControllerControl:
    """Control class."""

    def __init__(self, host, username, password):
        """Initialize."""
        self.host = host
        self.username = username
        self.password = password
        self.title = self.host.split('.')[0]

    async def __get_status(self):
        return json.loads(await _request(self.host, "?STATUS", self.username, self.password))

    async def authenticate(self) -> bool:
        """Test if we can authenticate with the host."""
        try:
            await self.__get_status()
            result = True
        except:
            result = False
        return result

    async def list(self):
        """List what we have"""

        result = []
        for name, value in (await self.__get_status()).items():
            result.append(CvrkyControllerControlItem(self.host, self.username, self.password, name, value[1]))
        return result

class CvrkyControllerControlItem:
    """Control class for single host."""

    def __init__(self, host, username, password, name, change_keyword):
        self.host = host
        self.username = username
        self.password = password
        self.name = name
        self.change_keyword = change_keyword

    async def toggle(self):
        await _request(self.host, "?{}".format(self.change_keyword), self.username, self.password)

    async def is_on(self):
        status = json.loads(await _request(self.host, "?STATUS"), self.username, self.password)
        return status[self.name][0]
