import random,csv,time,requests
from queue import Queue
from fake_useragent import UserAgent
from lxml import  etree
from threading import  Thread,Lock
class XiaomiSpider:
    def __init__(self):
        self.url = 'https://game.xiaomi.com/api/classify/getCategory?firstCategory=&secondCategory=&apkSizeMin=0&apkSizeMax=0&language=&network=-1&options=&page={}&gameSort=1'
        self.q = Queue()
        self.i = 0
        self.f = open('xiaomi.csv','a',newline='',encoding='utf-8')
        self.writer = csv.writer(self.f)
        self.lock = Lock()

    def get_page_number(self):
        for index in range(20,30):
            url = self.url.format(index)
            html_py = self.get_html_py(url)
            if html_py['errCode'] == 572:
                print(index)
                return index


    def get_html_py(self,url):
        html_py = requests.get(url=url,headers=self.get_header()).json()
        time.sleep(random.randint(1,3))
        return html_py

    def get_header(self):
        ua = UserAgent()
        headers={
            'User-Agent':ua.random,
            'cookie':'XSRF-TOKEN=omTo4DFAqjOWAEK7k2Gjr4ic; t_id=noimeih5_31a700fe-4e21-49b4-ba40-9bf0633baa8c; Hm_lvt_e851e68cf7b2da7b8231c5526a36f277=1679907984; LAST_RESIDENCE_TIMESTAMP=1679907990176; mac=02:42:0a:77:31:ca; Hm_lpvt_e851e68cf7b2da7b8231c5526a36f277=1679907990'
        }
        return headers

    def url_in(self):
       for page in range(1,self.get_page_number()):
           url = self.url.format(page)
           self.q.put(url)

    def get_data(self):
        while True:
            if not self.q.empty():
                url = self.q.get()
                html_py = self.get_html_py(url)
                self.parse_html(html_py)
            else:
                break

    def parse_html(self,html_py):
        app_list = []
        for app in html_py['gameList']:
            name = app['gameInfo']['displayName']
            two_url = 'https://game.xiaomi.com/game/' + str(app['gameInfo']['gameId'])
            down_url = app['gameInfo']['gameApk']
            print(name,two_url)
            self.i += 1
            introduce = self.get_two_html(two_url)
            app_list.append((name,down_url,introduce))
        self.lock.acquire()
        self.writer.writerows(app_list)
        self.lock.release()
        print('写完一页')

    def get_two_html(self,two_url):
        html=requests.get(url=two_url,headers=self.get_header()).text
        re_dbs = '//div[@class="section-game-desc"]/p/text()|//meta[@name="description"]/@content'
        pattern = etree.HTML(html)
        r_list = pattern.xpath(re_dbs)
        introduce = r_list[0] if r_list else None
        time.sleep(random.randint(1,3))
        return introduce

    def run(self):
        self.url_in()
        t_list = []
        for i in range(10):
            t=Thread(target=self.get_data())
            t_list.append(t)
            t.start()
        for t in t_list:
            t.join() # 释放
        self.f.close()

if __name__ == '__main__':
    spider = XiaomiSpider()
    spider.run()

