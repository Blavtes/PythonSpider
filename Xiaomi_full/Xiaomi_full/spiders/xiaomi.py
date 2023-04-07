import scrapy

from fake_useragent import UserAgent
from ..items import XiaomiFullItem

from ..pipelines import Xiaomi_MysqlPipeline
import requests,time,random
from hashlib import md5
class XiaomiSpider(scrapy.Spider):
    name = 'xiaomi'
    allowed_domains = ['game.xiaomi.com']
    start_urls = ['http://game.xiaomi.com/']
    url = 'https://game.xiaomi.com/api/classify/getCategory?firstCategory=&secondCategory=&apkSizeMin=0&apkSizeMax=0&language=&network=-1&options=&page={}&gameSort=1'

    # 重写父类方法
    def start_requests(self):
        number = self.get_page_number()
        m = Xiaomi_MysqlPipeline()
        for index in range(1, number):
            url = self.url.format(index)
            s = md5()
            s.update(url.encode())
            finger = s.hexdigest()
            if m.is_go_on(finger):
                yield scrapy.Request(url, callback=self.parse)

    def get_page_number(self):
        for index in range(20, 30):
            url = self.url.format(index)
            ua = UserAgent()
            headers = {
                'User-Agent': ua.random,
                'cookie': 't_id=noimeih5_31a700fe-4e21-49b4-ba40-9bf0633baa8c; XSRF-TOKEN=SoJU6IBwUUhRi49piP0I_JTK; Hm_lvt_e851e68cf7b2da7b8231c5526a36f277=1679907984,1680513559; LAST_RESIDENCE_TIMESTAMP=1680578184725; mac=02:42:0a:77:31:ca; Hm_lpvt_e851e68cf7b2da7b8231c5526a36f277=1680578192'
            }
            html_py = requests.get(url=url, headers=headers).json()
            time.sleep(random.randint(1, 3))
            if html_py['errCode'] != 200:
                print(index)
                return index

    def parse(self, response):
        html_py = response.json()
        item = XiaomiFullItem()
        for app in html_py['gameList']:
            item['name'] = app['gameInfo']['displayName']
            item['two_url'] = 'http://game.xiaomi.com/game/' + str(app['gameInfo']['gameId'])
            item['down_url'] = app['gameInfo']['gameApk']
            yield item


