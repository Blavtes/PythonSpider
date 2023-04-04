import scrapy
from ..items import XiaomiItem


class XiaomiSpider(scrapy.Spider):
    name = 'xiaomi'
    allowed_domains = ['game.xiaomi.com']
    number = 1
    base_url = 'https://game.xiaomi.com/api/classify/getCategory?firstCategory=&secondCategory=&apkSizeMin=0&apkSizeMax=0&language=&network=-1&options=&page={}&gameSort=1'
    start_urls = [base_url.format(number)]

    def parse(self, response):
        html_py = response.json()
        item = XiaomiItem()
        for app in html_py['gameList']:
            item['name'] = app['gameInfo']['displayName']
            item['two_link'] = 'https://game.xiaomi.com/game/' + str(app['gameInfo']['gameId'])
            item['down_url'] = app['gameInfo']['gameApk']
            yield item
        self.number += 1
        if self.number <= 20:
            nexturl = self.base_url.format(self.number)
            # 交给调度器进入队列
            yield scrapy.Request(
                url=nexturl,
                # 指定解析函数
                callback=self.parse
            )
