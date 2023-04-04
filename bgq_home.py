from urllib import request
from fake_useragent import  UserAgent
from lxml import etree
from hashlib import  md5
import re, time, random, pymysql

class BqgSpider():
    def __init__(self, name):
        self.db = pymysql.connect(host='localhost', user='root', password='YYyangyong00', database='filmaskydb',
                                  charset='utf8')
        self.cursor = self.db.cursor()

        self.ename = name
    def get_header(self):
        us = UserAgent();
        headers = {'User-Agent':us.random}
        return headers

    def get_html(self, url):
        req = request.Request(url = url, headers=self.get_header())
        res = request.urlopen(req)
        html = res.read().decode('utf-8')
        return html

    def re_func(self, html, re_dbs):
        pattern = re.compile(re_dbs, re.S)
        r_list = pattern.findall(html)
        return r_list

        # xpath 解析

    def xpath_func(self, html, xpath_dbs):
        parse_html = etree.HTML(html)
        r_list = parse_html.xpath(xpath_dbs)
        return r_list

     # 4、判断是否已下载

    def is_go_on(self, finger):
        sel = 'select * from request_finger where finger=%s'
        r = self.cursor.execute(sel, [finger])
        if not r:
            return True
        else:
            return False

    def parse_html(self, html):
        # re_dbs = r'<dd><a href ="(.*?)">(.*?)</a></dd>'
        # title_list = self.re_func(html, re_dbs)
        # l = []
        # for item in title_list:
        #     url = 'https://www.bqg70.com'+ item[0]
        #     name = item[1]
        #     re_dbs2 = r'<div id="chaptercontent" class="Readarea ReadAjax_content">(.*?)<p class="readinline">'
        #     content_list = self.re_func(self.get_html(url), re_dbs2)
        #     tem = (name, content_list[0])
        #     print(name)
        #     l.append(tem)

            # 方法2
        xpath_dbs = '//div[@class="listmain"]/dl//dd'
        title_list = self.xpath_func(html, xpath_dbs)
        print(title_list)
        with open(self.ename, mode='a', encoding='utf-8') as f:
            for item in title_list:
                xpath_url = './a/@href'
                url_list = item.xpath(xpath_url)
                xpath_name='./a/text()'
                name_list=item.xpath(xpath_name)
                if len(url_list) > 0:
                    if url_list[0].strip() == "javascript:dd_show()":
                        continue
                    two_url = 'https://www.bige7.com' + url_list[0].strip()
                    s = md5()
                    s.update(two_url.encode())
                    finger = s.hexdigest()
                    if self.is_go_on(finger):
                        xpath_dbs2 = '//div[@id="chaptercontent"]/text()'
                        content_list = self.xpath_func(self.get_html(two_url), xpath_dbs2)
                        data = ""
                        data = name_list[0] + '\n'
                        data += '\n'.join(content_list)
                        f.write(data)
                        print('报存成功....{}'.format(name_list[0]),end = "")
                        ins = 'insert into request_finger values(%s)'
                        self.cursor.execute(ins, [finger])
                        self.db.commit()

    def parse_html_save(self, html):
        re_dbs = r'<dd><a href ="(.*?)">(.*?)</a></dd>'
        title_re = r'<span class="title">(.*?)</span>'
        title_list = self.re_func(html, re_dbs)
        title_l = self.re_func(html, title_re)
        title = title_l[0] + '.txt'
        print(title_l)
        print(title)

        with open(title, 'a', encoding='utf-8') as f:
            for item in title_list:
                url = 'https://www.bqg70.com'+ item[0]
                name = item[1]
                re_dbs2 = r'<div id="chaptercontent" class="Readarea ReadAjax_content">(.*?)<p class="readinline">'
                content_list = self.re_func(self.get_html(url), re_dbs2)
                item = (name, content_list[0])
                data = ''
                data += item[0] + '\n'
                data += '\n'.join(item[1].strip().replace('　　','').split('<br /><br />'))
                f.write(data)
                print('\r爬取成功......{}'.format(data), end='')
                print('\r爬取成功......{}'.format(item[0]),end='')


    def run(self, url):
        # self.parse_html_save(self.get_html(url))
        self.parse_html(self.get_html(url))
        # with open(self.ename, mode='a', encoding='utf-8') as f:
        #     for item in L:
        #         data = ''
        #         data += item[0]+'\n'
        #         data += item[1]


if __name__ == '__main__':
    url = 'https://www.bqg70.com/book/39240/'
    name = '万相之王'
    spider = BqgSpider(name+'txt')
    spider.run(url)
