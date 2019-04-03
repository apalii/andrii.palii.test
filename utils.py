import aiohttp
from bs4 import BeautifulSoup


class WebClient:
    """
    Simple async web client which implements GET method
    https://docs.aiohttp.org/en/stable/client_quickstart.html#make-a-request
    """
    def __init__(self):
        self._session = aiohttp.ClientSession()

    async def get(self, url, data_type='json'):
        async with self._session.get(url, ssl=True) as response:
            if data_type == 'text':
                return await response.text()
            return await response.json()

    async def close(self):
        await self._session.close()


class Parser:
    """
    Simple parser for the requested web site :
    https://play.google.com/store/apps/category/GAME
    """
    def __init__(self, data):
        self.data = data

    def get_json(self):
        """
        Method returns dict with games categories as a key and list of the games which belongs to the category,
        for further serialization to JSON in aiohttp.web.json_response
        """
        soup = BeautifulSoup(self.data, 'html.parser')
        categories = soup.find_all("div", class_="uTDLzc")
        parsed_data = {
            cat.find('h2', class_='C7Bf8e bs3Xnd').get_text(): [game.get_text() for game in
                                                                cat.find_all('div', "WsMG1c nnK0zc")]
            for cat in categories
        }
        return parsed_data
