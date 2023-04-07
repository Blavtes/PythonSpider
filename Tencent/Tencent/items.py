# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class TencentItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    job_name = scrapy.Field()
    job_CategoryName = scrapy.Field()
    job_Responsibility = scrapy.Field()
    job_Requirement = scrapy.Field()
    job_LocationName = scrapy.Field()
    job_LastUpdateTime = scrapy.Field()
