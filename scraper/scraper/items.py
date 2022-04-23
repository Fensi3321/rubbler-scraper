# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class OfferItem(scrapy.Item):
    id = scrapy.Field()
    title = scrapy.Field()
    price = scrapy.Field()
    link = scrapy.Field()
    #####################
    model = scrapy.Field()
    added = scrapy.Field()
    power = scrapy.Field()
    displacement = scrapy.Field()
    fuel = scrapy.Field()
    productionYear = scrapy.Field()
    gearbox = scrapy.Field()
    body = scrapy.Field()
    condition = scrapy.Field()

