import requests, time, random,os
from lxml import etree
from fake_useragent import UserAgent
import pymysql

class SHiciSpider():
    def __init__(self):
        self.url = 'https://so.gushiwen.cn/gushi/tangshi.aspx'
        self.db = pymysql.connect(host='localhost', user='root', password='YYyangyong00', database='gushichi',
                                  charset='utf8')
        self.cursor = self.db.cursor()

    #得到页面字符串
    def get_html(self, url):
        ua = UserAgent()
        headers = {'User-Agent':ua.random}
        res = requests.get(url=url,headers=headers)
        res.encoding = 'utf-8'
        html = res.text
        return html
    # 得到二级页面的链接
    def get_twourl(self,one_html):
        xpath_db = '//div[@class="sons"]/div[@class="typecont"]/span'
        r_list = self.xpath_func(xpath_db, one_html)
        for item in r_list:
            url = 'https://so.gushiwen.cn' +item.xpath('./a/@href')[0]
            self.parse_html(url)
            return

    #解析
    def parse_html(self,url):
        two_html = self.get_html(url)
        xpath_dbs = '//div[@id="sonsyuanwen"]'
        r_list = self.xpath_func(xpath_dbs,two_html)
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

            print('=== 注释 '%ss + zhu_pm3_id)
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

                shici = name + '\n' + author + '\t' + caodai + '\n' + ''.join(contson).strip()
                self.save_data(name,shici,mp3,mp3_name,zhushi_mp3,zhushi_name)
    # mp3
    def get_mp3(self,mp3_url):
        ua = UserAgent()
        headers = {'User-Agent':ua.random}
        mp3 = requests.get(url=mp3_url,headers=headers).content
        return mp3
    # save

    # 4、判断是否已下载

    def is_go_on(self, finger):
        sel = 'select * from sctype where finger=%s'
        r = self.cursor.execute(sel, [finger])
        if not r:
            return True
        else:
            return False

    def save_data(self,name,shici,mp3,mp3_name,zhushi_mp3,zhushi_name):
        dir = '诗词/{}/'.format(name)
        if not os.path.exists(dir):
            os.makedirs(dir)
        with open(dir+name+'.txt','w',encoding='utf-8') as f:
            f.write(shici)
        with open(dir+name+'.mp3','wb') as f:
            f.write(mp3)
        with open(dir + name + '_注释.mp3', 'wb') as f:
            f.write(zhushi_mp3)

    def xpath_func(self,xpath_dbs,html):
        parse_html = etree.HTML(html)
        r_list = parse_html.xpath(xpath_dbs)
        return r_list
    def run(self):
        self.get_twourl(self.get_html(self.url))

if __name__ == '__main__':
    sHiciSpider = SHiciSpider()
    sHiciSpider.run()
