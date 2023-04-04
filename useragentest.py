from urllib import request,parse
import time,random
from useragents import ug_list
# from fake_useragent import UserAgent

class TiebaSpider():
    def __init__(self):
        self.url = 'https://tieba.baidu.com/f?{}'

    #1得到页面
    def get_html(self, url):
        headers = {
            'User-Agent': random.choice(ug_list)}
        req = request.Request(url=url, headers=headers)
        res = request.urlopen(req)
        html = res.read().decode('utf-8')
        return html

    def parse_html(self):
        pass
    def save_html(self, filename, html):
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(filename)

    def run(self):
        name = input('输入贴吧名：')
        begin = int(input('起始页:'))
        end = int(input('结束页：'))

        for page in range(begin, end + 1):
            pn = (page - 1) * 50
            parses = {
                'kw': name,
                'pn': str(pn)
            }
            params = parse.urlencode(parses)
            filename = '{}-第{}页.html'.format(name, page)
            url = self.url.format(params, pn)
            print(url)
            html = self.get_html(url)
            print(html)
            # self.save_html(filename, html)gl
            time.sleep(random.randint(1, 3))

if __name__ == '__main__':
    start = time.time()
    spider = TiebaSpider()
    spider.run()
    end = time.time()
    print('执行时间%.2f' % (end - start))


