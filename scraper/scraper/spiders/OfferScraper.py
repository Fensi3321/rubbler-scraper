import logging
from hashlib import md5
import scrapy

from ..items import OfferItem


class OfferscraperSpider(scrapy.Spider):
    name = 'OfferScraper'
    allowed_domains = ['olx.pl']

    def start_requests(self):
        urls = [
            'https://www.olx.pl/motoryzacja/samochody/bmw/seria-3/',
            'https://www.olx.pl/motoryzacja/samochody/honda/civic/'
        ]

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response, **kwargs):
        for offer in response.css('.offer-wrapper'):
            item = OfferItem()

            item['id'] = md5((offer.css('a.link::attr(href)').get().split('#')[0]).encode('utf-8')).hexdigest()
            item['title'] = offer.css('.link strong::text').get()
            item['price'] = offer.css('.price strong::text').get().replace(' ', '').replace('zł', '')
            item['link'] = offer.css('a.link::attr(href)').get()

            request = scrapy.Request(url=item['link'], callback=self.parse_offer_details)
            request.meta['offer-meta'] = item

            yield request

    def parse_offer_details(self, response):
        item = response.meta['offer-meta']
        item['added'] = response.css('span.css-19yf5ek::text').get()

        offer_attrib_list = response.css('.css-sfcl1s li p::text').getall()

        logging.info(offer_attrib_list)

        item = self.map_attrib(offer_attrib_list, item)

        yield item

    def map_attrib(self, attrib_list, item):
        attrib_dict = {}
        for attrib in attrib_list:
            attrib_tokens = attrib.split(':')
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
