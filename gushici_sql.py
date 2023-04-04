import requests, time, random
from lxml import etree
from fake_useragent import UserAgent
import pymysql
from hashlib import  md5

class SHiciSpider():
    def __init__(self):
        self.url = 'https://so.gushiwen.cn/shiwens/'
        self.db = pymysql.connect(host='localhost', user='root', password='YYyangyong00', database='gushichi',
                                  charset='utf8')
        self.cursor = self.db.cursor()
        self.page=1
    #得到页面字符串
    def get_html(self, url):
        ua = UserAgent()
        headers = {'User-Agent':ua.random,
                   'Cookie':'Hm_lpvt_9007fab6814e892d3020a64454da5a55=1679478771; Hm_lvt_9007fab6814e892d3020a64454da5a55=1679383017; __bid_n=18703074486dd5a7ee4207; FPTOKEN=PMe2ZO6BESsrlpvm3I5jYJOfrCUv35ehmOEEfVtGWKYngVw89RXg8lT0dgh3mGHI0S5Et5y1WLaoSzAO1Nz7frTxFFpeZmkw1c4JJ1osCvD5YlweJjnccvZz/hK1aOFYq4HqonZA9bGwAOIaOyKaYusAhDpyEbhfbLGRA4MvS5BbEBxQdqJDg0b4cD24K1Q2O6Yf3PIjPb3HhQcHXeFygJ4WeshVjZB6M5fkW9PaL6kkD0fuPln19zvQFgTduTsocC7mleD0BSUPeOtcIyQ9Qki3CV40cfkoyTHJsRGaYEIU8W7B31r/JuYPC/zZc3uWlLTvCfsJ/LHGaHfNsAXVNDsTr77LXn1w5g1RjYdtusVrwD2RmnRRA4cpeR46WkY07pzgOF+WjJTPtiHJq5agoQ==|oqg1u6EQcRwQdqitDEy4MIdnNCIga5pMtMmLty2fYxQ=|10|09ccd99cfbe94f0c33cbf6a9b4b75a5a; login=flase; ticketStr=209556096%7cgQEf8DwAAAAAAAAAAS5odHRwOi8vd2VpeGluLnFxLmNvbS9xLzAycVNhX1FxbGVkN2kxczZEMDFBMW0AAgQGWhlkAwQAjScA; wxopenid=defoaltid; ASP.NET_SessionId=nlruqq3howcrucajeg3qq3yi'}
        res = requests.get(url=url,headers=headers)
        res.encoding = 'utf-8'
        html = res.text
        return html
    # 得到二级页面的链接
    def get_twourl(self,one_html):
        xpath_db = '//div[@class="titletype"]/div[@id="type2"]/div[@class="sright"]'
        r_list = self.xpath_func(xpath_db, one_html)[0]
        u = r_list.xpath('./a/text()')
        for item in u:
            self.get_treeurl(item,self.page)


    def get_treeurl(self,name,page):
        url = 'https://so.gushiwen.cn/shiwens/default.aspx?page={}&tstr=&astr={}&cstr=&xstr='.format(page,name)
        s = md5()
        s.update(url.encode())
        finger = s.hexdigest()
        print(url)
        if self.is_go_on(finger,url):
            # https://so.gushiwen.cn/shiwens/default.aspx?page=2&tstr=&astr=李白&cstr=&xstr=

            tree_html = self.get_html(url)
            xpath_dbs = '//div[@id="leftZhankai"]/div[@class="sons"]'
            r_list = self.xpath_func(xpath_dbs, tree_html)
            if r_list:
                self.page += 1
            else:
                self.page = 1
                return
            for item in r_list:
                time.sleep(random.randint(1, 3))
                title = item.xpath('./div[@class="cont"]/p/a/b/text()')
                author = item.xpath('./div[@class="cont"]/p[@class="source"]/a[1]/text()')
                caodai = item.xpath('./div[@class="cont"]/p[@class="source"]/a[2]/text()')
                contson = item.xpath('./div[@class="cont"]/div[@class="contson"]/p/text()')
                if len(contson) == 0:
                    contson = item.xpath('./div[@class="cont"]/div[@class="contson"]/text()')

                mp3_id = item.xpath('./div[@class="tool"]/div[4]/a/@href')[0].split("('")[-1].split("'")[0]
                play_html = self.get_html('https://so.gushiwen.cn/viewplay.aspx?id=' + mp3_id)
                shicidstr = title[0]+author[0]
                s = md5()
                s.update(shicidstr.encode())
                shiciid = s.hexdigest()
                xpath_dbs_mp3 = '//audio/@src'
                content = ''.join(contson).strip()
                if self.xpath_func(xpath_dbs_mp3, play_html):
                    mp3_url = self.xpath_func(xpath_dbs_mp3, play_html)[0]
                    print(mp3_url, title)
                    mp3_name = mp3_url.split('/')[-1]
                    mp3 = self.get_mp3(mp3_url)

                    self.save_data(title, author, caodai, content, mp3_id, mp3_url, mp3, finger,shiciid,url)
                else:
                    self.save_data(title, author, caodai, content, mp3_id, "", "", finger, shiciid, url)
            self.get_treeurl(name,self.page)
        else:
            self.get_treeurl(name, page+1)
    #解析
    def parse_html(self,url):
        two_html = self.get_html(url)
        xpath_dbs = '//div[@id="sonsyuanwen"]'
        r_list = self.xpath_func(xpath_dbs,two_html)
        s = md5()
        s.update(url.encode())
        finger = s.hexdigest()
        if self.is_go_on(finger,url):
            for item in r_list:
                name = item.xpath('./div[@class="cont"]/h1/text()')[0]
                author = item.xpath('./div[@class="cont"]/p[@class="source"]/a[1]/text()')[0]
                caodai = item.xpath('./div[@class="cont"]/p[@class="source"]/a[2]/text()')[0]
                contson = item.xpath('./div[@class="cont"]/div[@class="contson"]/text()')
                mp3_id = item.xpath('./div[@class="tool"]/div[4]/a/@href')[0].split("('")[-1].split("'")[0]
                play_html = self.get_html('https://so.gushiwen.cn/viewplay.aspx?id='+mp3_id)
                #译文及注释
                xpath_zhushi = '//div[@class="contyishang"]'
                zhushi_list = self.xpath_func(xpath_zhushi, two_html)
                ss = zhushi_list[0].xpath('./p/text()')
                zhu_pm3_id = zhushi_list[0].xpath('./div[1]/a/@href')[0].split("(")[-1].split(",")[0]


                zhushi_html = self.get_html('https://so.gushiwen.cn/fanyiplay.aspx?id=' + zhu_pm3_id)

                # 'https://so.gushiwen.cn/fanyiplay.aspx?id=12850'
                xpath_dbs_mp3 = '//audio/@src'
                if self.xpath_func(xpath_dbs_mp3,play_html):
                    mp3_url = self.xpath_func(xpath_dbs_mp3, play_html)[0]
                    print(mp3_url, name)
                    mp3_name = mp3_url.split('/')[-1]
                    mp3 = self.get_mp3(mp3_url)
                    zhushi_mp3_url = self.xpath_func(xpath_dbs_mp3, zhushi_html)[0]
                    zhushi_name = mp3_url.split('/')[-2]
                    zhushi_mp3 = self.get_mp3(zhushi_mp3_url)

                    content = ''.join(contson).strip()
                    self.save_data(name,author,caodai,content,mp3_id,mp3_url,mp3,zhu_pm3_id,zhushi_mp3_url,zhushi_mp3,finger)
                else:
                    print('=== 注释 {}'.format( mp3_id))
                    self.save_data(name,author,caodai,content,mp3_id,"","","","","",finger)

    # mp3
    def get_mp3(self,mp3_url):
        ua = UserAgent()
        headers = {'User-Agent':ua.random}
        mp3 = requests.get(url=mp3_url,headers=headers).content
        return mp3
    # save

    # 4、判断是否已下载
    def is_go_on(self, finger,url):
        sel = 'select * from sctype where finger=%s'
        r = self.cursor.execute(sel, [finger])
        if not r:
            sctype = 'insert into sctype values(%s,%s,%s)'
            self.cursor.execute(sctype, [0, url, finger])
            self.db.commit()
            return True
        else:
            return False

    def save_data(self,title, author, caodai, content, mp3_id, mp3_url, mp3, finger,shiciid,url):
        print(title, author, caodai, content, mp3_id, mp3_url, shiciid, url)


        #shiciid,古诗名，作者，朝代，MP3_id,注释Id
        shici = 'insert into shici values(%s,%s,%s,%s,%s,%s,%s)'
        self.cursor.execute(shici, [0,shiciid,title,author,caodai, mp3_id,""])
        self.db.commit()

        #shiciid,mp3id,mp3_url,mp3内容，注释id,注释_url,注释音频内容，古诗内容,注释内容
        play = 'insert into play values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        self.cursor.execute(play, [0,shiciid,mp3_id,mp3_url,mp3,"","","",content,""])
        self.db.commit()


    def xpath_func(self,xpath_dbs,html):
        parse_html = etree.HTML(html)
        r_list = parse_html.xpath(xpath_dbs)
        return r_list
    def run(self):
        self.get_twourl(self.get_html(self.url))

if __name__ == '__main__':
    sHiciSpider = SHiciSpider()
    sHiciSpider.run()
