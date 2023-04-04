import scrapy

from ..items import DaomubijiItem
class DaomuSpider(scrapy.Spider):
    name = 'Daomu'
    allowed_domains = ['www.daomubiji.com']
    start_urls = ['http://www.daomubiji.com/']
    #第一级页面
    def parse(self, response):
        a_list = response.xpath('//li[contains(@id,"menu-item-20")]/a')
        for a in a_list:
            item = DaomubijiItem()
            item['title'] = a.xpath('./text()').get()
            link = a.xpath('./@href').get()
            # 扔给调度队列
            yield scrapy.Request(
                url = link,
                meta={
                    'item':item
                },
                callback=self.parse_two_page
            )
    def parse_two_page(self,response):
        item = response.meta['item']
        article_list = response.xpath('//article')
        for article in article_list:
            name = article.xpath('./a/text()').get()
            three_url = article.xpath('./a/@href').get()
            #继续交给调度器入队列
            yield scrapy.Request(
                url=three_url,
                meta={
                    'item':item,
                    'name':name
                },
                callback=self.parse_three_page
            )
    # 第三级存name，某一个章节名
    # 所有的数据在同一级保存
    def parse_three_page(self,response):
        item = response.meta['item']
        item['name'] = response.meta['name']
        p_list = response.xpath('//article/p/text()').extract() # 列表
        p_list.insert(0,item['name'])
        content = '\n'.join(p_list)
        item['content'] = content
        yield item