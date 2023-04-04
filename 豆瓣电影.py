import requests,time,random,re
from  fake_useragent import UserAgent
class DBdianyingSpider():
    def __init__(self):
        self.url = 'https://movie.douban.com/j/chart/top_list'

    def get_headers(self):
        ua = UserAgent()
        headers = {'User-Agent': ua.random}
        return headers
    def get_page(self,params):
        headers = self.get_headers()
        res = requests.get(url=self.url,headers=headers,params=params)
        res.encoding = 'utf-8'
        html_py = res.json()
        self.parse_page(html_py)
    def parse_page(self,html):
        item = {}
        for one in html:
            item['name'] = one['title'].strip()
            item['score'] = one['score'].strip()
            print(item)
    def total_number(self,type):
        url = 'https://movie.douban.com/j/chart/top_list_count?type={}&interval_id=100%3A90'.format(type)
        headers = self.get_headers()
        html_py = requests.get(url=url,headers=headers).json()
        total = int(html_py['total'])
        return total
    def get_all_type_films(self):
        url = 'https://movie.douban.com/chart'
        header = self.get_headers()
        html = requests.get(url=url,headers=header).text
        re_dbs = r'<a href=".*?type_name=(.*?)&type=(.*?)&.*?'
        patter = re.compile(re_dbs,re.S)
        r_list = patter.findall(html)
        type_dict = {}
        menu = ''
        for r in r_list:
            type_dict[r[0].strip()] = r[1].strip()
            menu += r[0] + '|'
        return type_dict,menu
    def run(self):
        type_dict,menu = self.get_all_type_films()
        menu = menu + '\n请做出您的选择'
        name = input(menu)
        type_number = type_dict[name]
        total = self.total_number(type_number)
        for start in range(0,(total + 1),20):
            params = {
                'type':type_number,
                'interval_id':'100:90',
                'action':'',
                'start':str(start),
                'limit':20
            }
            self.get_page(params)
            time.sleep(random.randint(1,3))
        print('电影数量',total)
if __name__ == '__main__':
    spider = DBdianyingSpider()
    spider.run()
