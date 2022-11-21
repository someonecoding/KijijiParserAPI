from urlparse import UrlParser
from adparse import AdParser
import asyncio
from random import randint
from db import insert_data



class Main:

    urlparser = UrlParser()
    adparser = AdParser()

    async def process_ad(self, adid):
        try:
            await asyncio.sleep(randint(1,15))
            result = await self.adparser.parse_ad(self.urls[adid]['url'])
            await insert_data('ads', {**result['base'], **result['details']})
            await insert_data('sellers', {**result['seller']})
            self.urls[adid]['status'] = True
            self.urls[adid]['result'] = result
        except:
            pass

    async def main(self):
        self.urls = await self.urlparser.gather_all_cities_ads()
        for key in self.urls.keys():
            self.urls[key] = {
                'url': self.urls[key],
                'status': False,
                'result': None
            }
        
        self.statuses = (value['status'] for value in self.urls.values())
        while not all(self.statuses):
            for k,v in self.urls.items():
                if not v['status']:
                    print(k, ' ', v['status'])
            tasks = [
                self.process_ad(key)
                for key, value in self.urls.items()
                if not value['status']
            ]
            await asyncio.gather(*tasks)
        
            

main = Main()
asyncio.run(main.main())

