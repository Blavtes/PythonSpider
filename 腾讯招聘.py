#https://careers.tencent.com/tencentcareer/api/post/Query?timestamp=1679898891138&countryId=&cityId=&bgIds=&productId=&categoryId=&parentCategoryId=&attrId=&keyword={}&pageIndex={}&pageSize=10&language=zh-cn&area=cn

import requests,json,time,random
from fake_useragent import UserAgent
from urllib import parse #处理中文字符
class TencentSpider():
    def __init__(self):
        self.one_url = 'https://careers.tencent.com/tencentcareer/api/post/Query?timestamp=1679898891138&countryId=&cityId=&bgIds=&productId=&categoryId=&parentCategoryId=&attrId=&keyword={}&pageIndex={}&pageSize=10&language=zh-cn&area=cn'
        self.two_url = 'https://careers.tencent.com/tencentcareer/api/post/ByPostId?timestamp=1679899597403&postId={}&language=zh-cn'
        #把数据抓取到item字典 统一保存到列表中
        self.item=[]
        self.f = open('tencent.json','a',encoding='utf-8')
        self.keyworld = ''
    #1、获取相应内容
    def get_page(self,url):
        ua = UserAgent()
        headers = {'User-Agent':ua.random}
        html = requests.get(url=url,headers=headers).text
        #json
        html_py = json.loads(html)
        return html_py
    #2、获取所有的数据一级页面的数据
    def parse_page(self,one_url):
        one_html_py = self.get_page(one_url)
        for job in one_html_py['Data']["Posts"]:
            item = {}
            post_id = job['PostId']
            tow_url = self.two_url.format(post_id)
            item['name'] ,item['duty'],item['require'] = self.parse_two_page(tow_url)
            print(item)
            self.item.append(item)
    #3、解析二级页面
    def parse_two_page(self,two_url):
        two_html_py = self.get_page(two_url)
        #名字
        name = two_html_py['Data']['RecruitPostName']
        duty = two_html_py['Data']['Responsibility']
        require = two_html_py['Data']['Requirement']
        return name,duty,require
    #4、获取分页总数
    def get_number(self):
        url = self.one_url.format(self.keyworld,1)
        html_py = self.get_page(url)
        number = html_py['Data']['Count']
        if number//10 == 0:
            return number/10
        return int(number/10)+1
    #5、主函数
    def run(self):
        keyword = input('input job type：')
        parse.quote(keyword)
        self.keyworld = keyword
        number = self.get_number()
        print('总页码：',number)
        for page in range(1,3):
            one_url = self.one_url.format(keyword,page)
            self.parse_page(one_url)

        #save
        json.dump(self.item,self.f,ensure_ascii=False)
        self.f.close()
if __name__=='__main__':
    tencent = TencentSpider()
    tencent.run()