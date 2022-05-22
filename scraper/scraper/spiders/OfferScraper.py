import datetime
import logging
import scrapy

from ..util.url_utils import create_url
from hashlib import md5
from ..items import OfferItem
from pymongo import MongoClient

client = MongoClient(host='localhost', port=27017, username='root', password='123')
base_url = 'https://olx.pl'

def get_urls(**kwargs) -> list[str]:
    db = client['rubbler']
    cars_collection = db['cars']

    car = cars_collection.find_one({'model': kwargs['model']})

    url = create_url(car['make'], [car['model']])

    return [url]


class OfferscraperSpider(scrapy.Spider):
    name = 'OfferScraper'
    allowed_domains = ['olx.pl']

    def start_requests(self):
        #urls = get_urls(model='prelude')
        urls = ['https://www.olx.pl/d/motoryzacja/samochody/honda/prelude']

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response, **kwargs):
        for offer in response.css('.css-19ucd76'):
            item = OfferItem()
            price = offer.css('p.css-l0108r-Text::text').get()
            link = offer.css('a.css-1bbgabe::attr(href)').get()
            title = offer.css('h6.css-v3vynn-Text::text').get()

            if price is None or link is None or title is None:
                continue

            item['title'] = title
            item['price'] = price
            item['link'] = base_url + link

            request = scrapy.Request(url=item['link'], callback=self.parse_offer_details)
            request.meta['offer-meta'] = item

            yield request

    def parse_offer_details(self, response):
        item = response.meta['offer-meta']

        item['added'] = response.css('span.css-19yf5ek::text').get()
        item['make'] = response.css('ol.css-2tdfce a::text').getall()[3]

        offer_attrib_list = response.css('.css-sfcl1s li p::text').getall()

        item = self.map_attrib(offer_attrib_list, item)

        yield item

    def map_attrib(self, attrib_list, item):
        attrib_dict = {}
        for attrib in attrib_list:
            attrib_tokens = attrib.split(': ')
            attrib_dict[attrib_tokens[0]] = attrib_tokens[1]

        item['model'] = attrib_dict.get('Model', None)
        item['power'] = attrib_dict.get('Moc silnika', None)
        item['displacement'] = attrib_dict.get('Poj. silnika', None)
        item['fuel'] = attrib_dict.get('Paliwo', None)
        item['productionYear'] = attrib_dict.get('Rok produkcji', None)
        item['gearbox'] = attrib_dict.get('Skrzynia biegów', None)
        item['body'] = attrib_dict.get('Typ nadwozia', None)
        item['condition'] = attrib_dict.get('Stan techniczny', None)

        return item
