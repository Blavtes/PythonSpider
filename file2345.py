from urllib import request
import re, time, random, pymysql
from  fake_useragent import UserAgent
from hashlib import  md5
# 2345 电影
class FileSpidder():
    def __init__(self):
        self.url = 'https://kan.2345.com/vip/list/--movie--0---{}.html'
        self.db = pymysql.connect(host='localhost', user='root', password='YYyangyong00',database='filmaskydb',charset='utf8')
        self.cursor = self.db.cursor()

    # 1、得到html
    def get_html(self, url):
        ua = UserAgent()
        headers = {'User-Agent': ua.random}
        req = request.Request(url=url, headers=headers)
        res = request.urlopen(req)
        html = res.read().decode('gb2312', 'ignore')  # ignore忽略编译不了的内容
        return html

    # 2、正则解析
    def re_func(self, re_dbs, html):
        patter = re.compile(re_dbs, re.S)
        r_list = patter.findall(html)
        return r_list

    # 3、数据解析
    def parse_html(self, one_url):
        on_html = self.get_html(one_url)
        re_dbs1 = '<a class="aPlayBtn" href="(.*?)" target="_blank"'
        link_list = self.re_func(re_dbs1, on_html)
        print("-----\n")
        print(link_list)
        for link in link_list:
            two_url = link
            # 判断是否已下载,首先给url 做md5
            s = md5()
            s.update(two_url.encode())  # 固定写法,字符串必须先encode 才能被MD5加密
            finger = s.hexdigest()  # 得到加密指纹
            if self.is_go_on(finger):
                # 1、爬取
                self.save_html(two_url)
                time.sleep(random.randint(1, 3))
                # 2、把爬取的二级url保存到指纹表
                ins = 'insert into request_finger values(%s)'
                self.cursor.execute(ins,[finger])
                self.db.commit()
            else:
                print('已下载')

    # 4、判断是否已下载
    def is_go_on(self, finger):
        sel = 'select * from request_finger where finger=%s'
        r = self.cursor.execute(sel, [finger])
        if not r:
            return True
        else:
            return False

    # 5、保存数据
    def save_html(self, two_url):
        two_html = self.get_html(two_url)
        re_dbs2 = r'<a href=\'(.*?)\' target="_blank" class="series-con-search series-con-play"'
        film_list = self.re_func(re_dbs2, two_html)
        re_dbs_title = r'<meta property="og:title" content="(.*?)"/>' # 可能会变动
        title = self.re_func(re_dbs_title, two_html)
        print("=====\n" + title[0])
        print(len(film_list))
        if len(film_list) >= 1:
            sql = 'insert into filmtab value(%s,%s)'
            L = list((title[0], film_list[0]))
            self.cursor.execute(sql,L)

    # 6、入口函数
    def run(self):
        for i in range(1, 2):
            url = self.url.format(i)
            self.parse_html(url)

if __name__ == '__main__':
    f = FileSpidder()
    f.run()