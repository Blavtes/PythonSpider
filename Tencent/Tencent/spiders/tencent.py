import random
import time
import scrapy
from ..items import TencentItem
from urllib import parse
import json
import requests
class TencentSpider(scrapy.Spider):
    name = 'tencent'
    allowed_domains = ['careers.tencent.com']
    # start_urls = ['http://careers.tencent.com/']
    one_url = 'https://careers.tencent.com/tencentcareer/api/post/Query?timestamp=1680596800712&countryId=&cityId=&bgIds=&productId=&categoryId=&parentCategoryId=&attrId=&keyword={}&pageIndex={}&pageSize=10&language=zh-cn&area=cn'
    two_url = 'https://careers.tencent.com/tencentcareer/api/post/ByPostId?timestamp=1680596854846&postId={}&language=zh-cn'
    user_input = input('输入工作岗位')
    user_input = parse.quote(user_input)
    url = one_url.format(user_input,1)
    # start_urls = [url] # 单线程需要 # 多线程重写 start_requests()
    number = 0

    def start_requests(self):
        # 单独获取总页数
        total = self.get_total(self.user_input)
        print(total) #
        for index in range(1,1+1):
            url = self.one_url.format(self.user_input,index)
            yield scrapy.Request(
                url=url,
                callback=self.parse_one_page
            )
    def get_total(self,user_input):
        url = self.one_url.format(user_input,1)
        html_py = requests.get(url=url).json()
        count =  html_py['Data']['Count']
        if count % 10 == 0:
            total = count // 10
        else:
            total = count // 10 + 1
        return total
    def parse_one_page(self, response):
        # response 返回的是json字符串
        html = response.text
        # json 转成python格式
        html_py = json.loads(html)
        for job in html_py['Data']['Posts']:
            post_id = job['PostId']
            url = self.two_url.format(post_id)
            yield scrapy.Request(
                url=url,
                callback=self.parse_two_page
            )
        # 获取总页数 单线程使用
        # count = html_py['Data']['Count']
        # if count%10 == 0:
        #     total = count//10
        # else:
        #     total = count//10 + 1
        # time.sleep(random.randint(1,3))
        # self.number += 1
        # print('第' + str(self.number) + '页完成')
        # # for index in range(2,total + 1): # range 前闭后开
        # for index in range(2, 3):  # range 前闭后开
        #     url = self.one_url.format(self.user_input,index)
        #     yield scrapy.Request(
        #         url=url,
        #         callback=self.parse # 返给自己
        #     )
    def parse_two_page(self,response):
        html_py = json.loads(response.text)['Data']
        item = TencentItem()
        item['job_name'] = html_py['RecruitPostName']
        item['job_CategoryName'] = html_py['CategoryName']
        item['job_Responsibility'] = html_py['Responsibility']
        item['job_Requirement'] = html_py['Requirement']
        item['job_LocationName'] = html_py['LocationName']
        item['job_LastUpdateTime'] = html_py['LastUpdateTime']
        yield item




