import scrapy
from ..items import DoubanItem

class DoubanSpider(scrapy.Spider):
    name = 'douban'
    allowed_domains = ['movie.douban.com']
    # start_urls = ['http://movie.douban.com/']
    url = 'https://movie.douban.com/top250?start={}&filter='

    def start_requests(self):
        for sn in range(0,250,25):
            url = self.url.format(sn)
            yield scrapy.Request(
                url=url,
                callback=self.parse
            )
    def parse(self, response):
        print(response.request.headers['User-Agent'])
        movie_list = response.xpath('//*[@id="content"]/div/div[1]/ol/li/div/div[2]')
        for movie in movie_list:
            item = DoubanItem()
            item['name'] = movie.xpath('./div[1]/a/span[1]/text()').get()
            yield item

