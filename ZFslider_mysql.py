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
        a_list = parse_html.xpath(xp_dbs)
        for a in a_list:
            title = a.xpath('./@title')[0]
            href = a.xpath('./@href')[0]
            if title.endswith('代码'):
                url = 'https://www.mca.gov.cn' + href
                print(url)
                if self.ifupdate(url):
                    self.get_true_url(url)
                    self.save_finger(url,title)
                else:
                    print("已下载")
                break
    def ifupdate(self,url):
        s=md5()
        s.update(url.encode())
        md5_url = s.hexdigest()
        sql = 'select * from finger where url=%s'
        row = self.cursor.execute(sql,[md5_url])
        if row:
            return False
        else:
            return True
    def get_true_url(self,url):
        html = requests.get(url=url,headers=self.header).text
        hre_dbs = 'window.location.href="(.*?)";'
        patter = re.compile(hre_dbs,re.S)
        true_url = patter.findall(html)[0]
        self.parse_html(true_url)
    def parse_html(self,url):
        html = requests.get(url=url,headers=self.header).text
        parse_html = etree.HTML(html)
        r_list = parse_html.xpath('//tr[@height="19"]')
        for r in r_list:
            code = r.xpath('./td[2]/text()|td[2]/span/text()')[0].strip()
            name = r.xpath('./td[3]/text()')[0].strip()
            with open('xingzheng.txt','a',encoding='utf-8') as f:
                f.write(name+',' + code +'\n')
            self.save_to_sql(name,code)
    def save_to_sql(self,name,code):
        if code[2:] == '0000':
            self.save_data('province',name,code)
        elif code[4:] == '00':
            self.save_data('city',name,code)
        else:
            self.save_data('county',name,code)
    def save_data(self,type,name,code):
        if type == 'province':
            sql = 'insert into '+type + ' values(%s,%s)'
            self.cursor.execute(sql,[code,name])
        else:
            sql = 'insert into ' + type + ' values(%s,%s,%s)'
            if type == 'city':
                self.cursor.execute(sql,[code,code[:2] + '0000',name])
            else:
                self.cursor.execute(sql, [code, code[:4] + '00', name])
        self.db.commit()
    def save_finger(self,url,title):
        s = md5()
        s.update(url.encode())
        m5 = s.hexdigest()
        sql = 'insert into finger value(%s,%s)'
        self.cursor.execute(sql,[m5,title])
        self.db.commit()

if __name__ == '__main__':
    sz = ZFSpiher()
    sz.get_false_url()