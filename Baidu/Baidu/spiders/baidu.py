import scrapy


class BaiduSpider(scrapy.Spider):
    name = 'baidu'
    allowed_domains = ['www.baidu.com']
    start_urls = ['http://www.baidu.com/']

    def parse(self, response):
        result = response.xpath('/html/head/title/text()').get() # 取字符串
        # result = response.xpath('/html/head/title/text()')[0]
        # result = response.xpath('/html/head/title/text()').extract_first()# 3.5 以前
        print('*'*50)
        print(result)
        print('*'*50)