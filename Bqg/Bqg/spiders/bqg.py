import scrapy
from ..items import BqgItem

class BqgSpider(scrapy.Spider):
    name = 'bqg'
    allowed_domains = ['www.biquqq.com']
    start_urls = ['https://www.biquqq.com/62_62346']

    def parse(self, response):
            print(response)
            item = BqgItem()
            dd_list = response.xpath('//*[@id="list"]/dl/dd')
            for dd in dd_list[9:]:
                item['name'] = dd.xpath('./a/text()').get().strip()
                item['url'] = dd.xpath('./a/@href').get().strip()
                # 利用生成器把item 放到管道文件中
                yield item
