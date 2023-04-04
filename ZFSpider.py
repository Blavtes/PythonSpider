import re

import requests,pymysql
from lxml import etree
from hashlib import md5

class ZFSpiher():
    def __init__(self):
        self.url = 'https://www.mca.gov.cn/article/sj/xzqh/2020/'
        self.header = {'User-Agent':'Mozilla/5.0'}
        self.db = pymysql.connect(host='localhost', user='root', password='YYyangyong00', database='zfdb',
                                  charset='utf8')
        self.cursor = self.db.cursor()
    
    def get_false_url(self):
        html = requests.get(url=self.url,headers=self.header).text
        xp_dbs = '//a[@class="artitlelist"]'
        parse_html = etree.HTML(html)
        a_link = parse_html.xpath(xp_dbs)
        for a in a_link:
            title = a.xpath('./@title')[0].strip()
            href = a.get('href')
            if title.endswith('代码'):
                link = 'https://www.mca.gov.cn' + href
                print(link)
                self.get_true_url(link)
                break

    def get_true_url(self,false_url):
        html = requests.get(url=false_url,headers=self.header).text
        re_dbs = 'window.location.href="(.*?)";'
        pattern = re.compile(re_dbs,re.S)
        true_url = pattern.findall(html)[0]
        self.parse_html(true_url)
    def parse_html(self,url):
        html = requests.get(url=url, headers=self.header).text
        xp_dbs = '//tr[@height="19"]'
        parse_html = etree.HTML(html)
        r_list = parse_html.xpath(xp_dbs)
        for r in r_list:
            code = r.xpath('./td[2]/text()|./td[2]/span/text()')[0]
            name = r.xpath('./td[3]/text()')[0]
            print(code, name)
            with open('行政编码.txt','a') as f:
                f.write(code + '\t' + name + '\n')

if __name__ == '__main__':
    zf = ZFSpiher()
    zf.get_false_url()