import aiohttp
from urlparse import UrlParser
import asyncio
from parser_session import ParserSession
from bs4 import BeautifulSoup
import re
from datetime import datetime
from utils import extract_seller_id
from anvilapi import anvil_get_profile, anvil_get_profile_phone
import json
from random import randint



class AdParser:

    def extract_apartment_base(self, soup):
        adid_re = re.compile('.*adId-.*')
        title_re = re.compile('.*title-.*')
        posted_re = re.compile('.*datePosted-.*')
        price__ut_wrapper_re = re.compile('.*priceWrapper-.*')
        utilities_re = re.compile('.*utilities-.*')
        description_re = re.compile('.*descriptionContainer-.*')
        sellerurl_re = re.compile('.*avatarLink-.*')

        adid = int(soup.find("a", {"class": adid_re}).string)
        title = soup.find("h1", {"class": title_re}).string
        location = soup.find("span", {"itemprop": 'address'}).string
        posted = datetime.strptime(soup.find("div", {"class": posted_re}).time['datetime'], '%Y-%m-%dT%H:%M:%S%f.000Z')
        
        price_ut_wrapper = soup.find("div", {"class": price__ut_wrapper_re})
        price_span = price_ut_wrapper.find("span")
        price = float(price_span.get('content')) if price_span.get('content') is not None else None
        utilities = price_ut_wrapper.find('span', {"class": utilities_re}).string
        description = soup.find("div", {"class": description_re}).find("div").text
        sellerid = extract_seller_id(soup.find('a', {"class": sellerurl_re})['href'])

        return {
            'adid': adid,
            'title': title,
            'location': location,
            'posted': posted,
            'price': price,
            'utilities': utilities,
            'description': description,
            'sellerid': sellerid,
        }

    def extract_apartment_details(self, soup):
        details_block_re = re.compile('.*itemAttributeCards-.*')
        cards_re = re.compile('.*root-.*')

        details_block = soup.find("div", {"class": details_block_re})
        cards_list = details_block.find_all("div", {"class": cards_re})
        for card in cards_list:
            title = card.find('h3').text
            
            if title == 'Overview':

                utilities_list = card.find("h4", string='Utilities Included').parent.find('ul')
                utilities = {
                    'hydro': False,
                    'heat': False,
                    'water': False
                }
                if utilities_list.string != 'Not Included':
                    for i in utilities_list:
                        uti_temp = i.find('svg')['aria-label']
                        uti_temp = uti_temp.split(":")
                        uti_name = uti_temp[1][1::].lower()
                        if uti_temp[0] == 'Yes':
                            utilities[uti_name] = True

                wifi = {
                    'internet': False,
                    'cable': False
                    }
                wifi_list = card.find("h4", string='Wi-Fi and More').parent.find('ul')
                for i in wifi_list:
                    if i.string == 'Internet':
                        wifi['internet'] = True
                    if i.string == 'Cable/TV':
                        wifi['cable'] = True
                
                parking = card.find("dt", string='Parking Included').parent.find('dd').string
                
                agreement = card.find("dt", string='Agreement Type').parent.find('dd').string.lower()
                
                try:
                    move_in_date = card.find("dt", string='Move-In Date').parent.find('dd').find('span').string
                except AttributeError:
                    move_in_date = None
                
                pets = card.find("dt", string='Pet Friendly').parent.find('dd').string
                if pets == 'Yes' or pets == 'Limited':
                    pets = True
                if pets == 'No':
                    pets = False


            elif title == 'The Unit':
                size = card.find("dt", string='Size (sqft)').parent.find('dd').string
                try:
                    size = int(size)
                except ValueError:
                    size = None
                
                furnished = card.find("dt", string='Furnished').parent.find('dd').string
                furnished = True if furnished == 'Yes' else False
                
                appliances = {
                    'laundry_iu': False,
                    'laundry_ib': False,
                    'dishwasher': False,
                    'fridge': False
                }
                appl_list = card.find("h4", string='Appliances').parent.find('ul')
                if appl_list.string != 'Not Included':
                    for i in appl_list:
                        if i.string == 'Laundry (In Unit)':
                            appliances['laundry_iu'] = True
                        elif i.string == 'Laundry (In Building)':
                            appliances['laundry_ib'] = True
                        elif i.string == 'Dishwasher':
                            appliances['dishwasher'] = True
                        elif i.string == 'Fridge / Freezer':
                            appliances['fridge'] = True
                
                cond = card.find("dt", string='Air Conditioning').parent.find('dd').string
                cond = True if cond == 'Yes' else False
                
                personal_space = {
                    'yard': False,
                    'balcony': False
                }
                personal_space_list = card.find("h4", string='Personal Outdoor Space').parent.find('ul')
                if personal_space_list.string != 'Not Included':
                    for i in personal_space_list:
                        if i.string == 'Yard':
                            personal_space['yard'] = True
                        elif i.string == 'Balcony':
                            personal_space['balcony'] = True
                        
                smoking = card.find("dt", string='Smoking Permitted').parent.find('dd').string
                if smoking == 'Yes' or smoking == 'Outdoors only':
                    smoking = True
                else:
                    smoking = False


        result = {
            **utilities,
            **wifi,
            'parking': parking,
            'agreement': agreement,
            'pets': pets,
            'size': size,
            'furnished': furnished,
            **appliances,
            'conditioning': cond,
            **personal_space,
            'smoking': smoking
        }

        return result

    async def extract_apartment_seller(self, soup, adid, vipurl):
        seller_wrapper_re = re.compile('.*itemInfoSidebar-.*')
        seller_div_re = re.compile('.*root-.*')
        seller_id_re = re.compile('.*link-.*')
        seller_info_re = re.compile('.*lines-.*')
        seller_stats_re = re.compile('.*grid-.*')
        seller_stats_text_re = re.compile('.*text-.*')

        seller_div = soup.find('div', {"class": seller_wrapper_re}).find("div", {"class": seller_div_re})
        sellerlink = seller_div.find("a", {"class": seller_id_re})
        sellerurl = sellerlink['href']
        sellerid = extract_seller_id(sellerurl)

        seller_profile = await anvil_get_profile(sellerid)
        seller_profile = json.loads(seller_profile['text'])[0]['data']['findProfile']
        seller_number = await anvil_get_profile_phone(adid, sellerid, vipurl, seller_profile['companyName'])
        seller_number = json.loads(seller_number['text'])[0]

        if 'errors' in seller_number.keys():
            seller_number = None
        else:
            seller_number = seller_number['data']['getDynamicPhoneNumber']['local']
        
        seller_profile['phone'] = seller_number

        return seller_profile

    async def parse_ad(self, url):
        session = ParserSession()
        r = await session.fetch(url, sleep=randint(1, 60))
        html = r.get('text')
        soup = BeautifulSoup(html, 'lxml')
        apartment_base = self.extract_apartment_base(soup)
        apartment_seller = await self.extract_apartment_seller(soup, apartment_base['adid'], url)
        apartment_details = self.extract_apartment_details(soup)

        result = {
            'base': apartment_base,
            'details': apartment_details,
            'seller': apartment_seller
        }

        return result