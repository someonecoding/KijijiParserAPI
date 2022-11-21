import aiohttp
import requests
import asyncio
from fake_headers import Headers
import json



class ParserSession:

    fake_headers = Headers(headers=True)
    session = aiohttp.ClientSession


    async def fetch(self, url: str, sleep: int = 0):
        async with self.session() as session:
            await asyncio.sleep(sleep)
            async with session.get(url=url, headers=self.fake_headers.generate()) as response:
                return {
                    'status': response.status,
                    'url': response.url,
                    'text': await response.text()
                }
    
    async def post(self, url: str, payload, sleep: int = 0):
        async with self.session() as session:
            await asyncio.sleep(sleep)
            async with session.post(url=url, headers=self.fake_headers.generate(), json=payload) as response:
                return {
                    'status': response.status,
                    'url': response.url,
                    'text': await response.text()
                }
