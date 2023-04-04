from urllib import request
from fake_useragent import UserAgent
import time,re
import csv
import pymysql
from lxml import etree

class BqgSpider():
    def __init__(self):
        self.url = 'https://www.bqg70.com/book/2749/'

    # get html
    def get_html(self,url):
        ua=UserAgent()
        headers={'User-Agent': ua.random,
                 'cookie': 'Hm_lvt_7069209d76184c3513ce3df5e48fdbd6=1678957304; Hm_lpvt_7069209d76184c3513ce3df5e48fdbd6=1678957312'
                 }
        req = request.Request(url=url, headers=headers)
        res = request.urlopen(req)
        html = res.read().decode('utf-8')
        return html



    # parse html
    def parse_html(self, html):
        #正则
        re_dbs = '<dd><a href ="(.*?)">(.*?)</a></dd>'
        pattern = re.compile(re_dbs, re.S)
        r_list = pattern.findall(html)
        print(r_list)
        self.save_mysql(r_list)

        # self.save_mysql(r_list)
    def save_text(self, r_list):
        # w 每次都重新保存一遍
        with open('bqg.csv','w',newline='') as f:
            writer = csv.writer(f)
            writer.writerows(r_list)

    def run(self):
        self.parse_html(self.get_html(self.url))

    def save_mysql(self,r_list):
        db = pymysql.connect(host='localhost',user='root',password='YYyangyong00',database='bqgbook',charset='utf8')
        cursor = db.cursor()
        L = []
        for tmp in r_list:
            t = (
                'https://www.bqg70.com'+tmp[0].strip(),
                tmp[1].strip()
            )
            # print(t)
            L.append(t)
        ins = 'insert into wxzwtab values(%s,%s)'
        cursor.executemany(ins, L)
        db.commit()
        cursor.close()
        db.close()

if __name__ == '__main__':
    start = time.time()
    bqgSpider = BqgSpider()
    bqgSpider.run()
    end = time.time()
    print('执行时间%.2f:'%(end - start) )