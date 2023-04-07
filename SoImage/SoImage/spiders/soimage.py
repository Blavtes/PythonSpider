import json

import scrapy
import os
from ..items import SoimageItem
class SoimageSpider(scrapy.Spider):
    name = 'soimage'
    allowed_domains = ['image.so.com']
    # start_urls = ['http://image.so.com/']
    url = 'https://image.so.com/zjl?sn={}&ch=beauty'
    dir = 'images/'
    if not os.path.exists(dir):
        os.makedirs(dir)
    # 重写
    def start_requests(self):
        for sn in range(0,30,30):
            url = self.url.format(sn)
            yield scrapy.Request(
                url=url,
                callback=self.parse
            )
    def parse(self, response):
        html_py = json.loads(response.text)
        item = SoimageItem()
        for img in html_py['list']:
            item['img_title'] = img['title']
            item['img_link'] = img['qhimg_url']
            yield item