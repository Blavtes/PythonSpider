# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class XiaomiFullItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    two_url = scrapy.Field()
    down_url = scrapy.Field()
