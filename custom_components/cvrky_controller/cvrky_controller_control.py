import aiohttp
import json


async def _request(host, path):
    async with aiohttp.ClientSession() as session:
        async with session.get(f"http://{host}{path}") as resp:
            if resp.status != 200:
                raise ValueError(f"Request failed with {resp.status}/{resp.reason}")
            return await resp.text()


class CvrkyControllerControl:
    """Control class."""

    def __init__(self, host):
        """Initialize."""
        self.host = host
        self.title = self.host.split('.')[0]

    async def __get_status(self):
        return json.loads(await _request(self.host, "?STATUS"))

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
            result.append(CvrkyControllerControlItem(self.host, name, value[1]))
        return result

class CvrkyControllerControlItem:
    """Control class for single host."""

    def __init__(self, host, name, change_keyword):
        self.host = host
        self.name = name
        self.change_keyword = change_keyword

    async def toggle(self):
        await _request(self.host, "?{}".format(self.change_keyword))

    async def is_on(self):
        status = json.loads(await _request(self.host, "?STATUS"))
        return status[self.name][0]
