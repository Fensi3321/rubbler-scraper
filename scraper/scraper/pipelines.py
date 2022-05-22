# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import datetime
import logging

from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
import pymongo


class CarCleanPipeline:
    def __init__(self):
        self.month_map = {
            'stycznia': 1,
            'lutego': 2,
            'marca': 3,
            'kwietnia': 4,
            'maja': 5,
            'czerwca': 6,
            'lipca': 7,
            'sierpnia': 8,
            'września': 9,
            'października': 10,
            'listopada': 11,
            'grudnia': 12
        }

    def process_item(self, item, spider):
        for key in item.keys():
            if key == 'displacement':
                item[key] = self.parse_displacement(item[key])
            if key == 'added':
                item[key] = self.parse_date(item[key])
            if key == 'price':
                item[key] = self.parse_price(item[key])
            if key == 'power':
                item[key] = self.parse_power(item[key])
            if key == 'productionYear':
                item[key] = self.parse_prod_year(item[key])

        return item

    def parse_prod_year(self, year):
        if year is None:
            return year

        return int(year.replace(' ', ''))

    def parse_displacement(self, data: str) -> int:
        if data is None:
            return data

        data = data.replace(' ', '')
        data = data.replace('cm³', '')

        return int(data)

    def parse_date(self, date: str) -> datetime:
        if 'dzisiaj' in date.lower():
            return datetime.datetime.today()

        date_tokens = date.split(' ')
        format = '%Y/%m/%d'
        input = date_tokens[2] + '/' + str(self.month_map[date_tokens[1]]) + '/' + date_tokens[0]

        return datetime.datetime.strptime(input, format)

    def parse_price(self, price: str) -> int:
        if price is None:
            return price

        price_tokens = price.split(' ')
        return int(price_tokens[0] + price_tokens[1])

    def parse_power(self, power: str):
        if power is None:
            return power

        power_tokens = power.split(' ')
        return int(power_tokens[0])


class CarMongoPipeline:
    def __init__(self):
        mongo = pymongo.MongoClient(host='localhost', port=27017, username='root', password='123')
        self.db = mongo['rubbler']

    def process_item(self, item, spider):
        valid = True

        for data in item:
            if not data:
                valid = False
                raise DropItem("Missing {0}!".format(data))

        if valid:
            self.db['offers'].insert_one(dict(item))
            logging.info('Offer added to MongoDB database!')

        return item
