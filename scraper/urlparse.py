import asyncio
from bs4 import BeautifulSoup
import typing
from collections import namedtuple
from parser_session import ParserSession
import random



City = namedtuple('City',
        ['city', 'parse_alias', 'kijiji_code']
    )

class UrlParser:

    def __init__(self):
        self.pages: int = 0
        self.urlmap: typing.Dict[str, typing.Dict[str, str]] = {}
        self.parse_cities = (
            City("Toronto", "city-of-toronto", "c37l1700273"),
            City("Quebec City", "ville-de-quebec", "c37l1700124"),
            City("Halifax", "city-of-halifax", "c37l1700321"),
            City("Fredericton", "fredericton", "c37l1700018"),
            City("Winnipeg", "winnipeg", "c37l1700192"),
            City("Victoria", "victoria-bc", "c37l1700173"),
            City("Charlottetown", "charlottetown-pei", "c37l1700119"),
            City("Regina", "regina", "c37l1700196"),
            City("Edmonton", "edmonton", "c37l1700203"),
            City("St. Johns", "st-johns", "c37l1700113"),
        )

    def get_city_ads_url(self, city: City, page: typing.Optional[int]=None) -> str:
        page_url_part = f"page-{page}/" if page is not None else ''
        return f'https://www.kijiji.ca/b-apartments-condos/{city.parse_alias}/{page_url_part}{city.kijiji_code}'

    async def get_max_page(self, city: City) -> int:
        session = ParserSession()

        base_city_url = self.get_city_ads_url(city, 100)

        r = await session.fetch(base_city_url)

        max_page = str(r.get('url'))
        max_page = max_page.split('?')
        max_page = max_page[0].split('/')
        max_page = max_page[-2][5::]

        return int(max_page)


    async def retrieve_ads_urls(self, page):
        session = ParserSession()

        to_sleep = random.randint(0, 5)
        r = await session.fetch(page, sleep=to_sleep)
        html = r.get('text')
        soup = BeautifulSoup(html, "lxml")

        ads = soup.findAll("div", {"data-listing-id": True})
        page_urlmap = {}
        for i in ads:
            page_urlmap[i['data-listing-id']] = 'https://www.kijiji.ca' + i['data-vip-url']
        if len(page_urlmap) == 0:
            await asyncio.sleep(random.randint(2, 15))
            return await self.retrieve_ads_urls(page)
        else:
            return page_urlmap

    async def gather_city_ads(self, city: City):
        max_page = await self.get_max_page(city)
        results = {}

        tasks = (self.retrieve_ads_urls(self.get_city_ads_url(city, i)) for i in range(1, max_page+1))
        gathered = asyncio.gather(*tasks)
        parsed = await gathered
        for i in parsed:
            results.update(i)

        return results

    async def gather_all_cities_ads(self):
        result = {}

        tasks = (self.gather_city_ads(city) for city in self.parse_cities)
        gathered = asyncio.gather(*tasks)
        parsed = await gathered

        for i in parsed:
            result.update(i)
        
        return result
