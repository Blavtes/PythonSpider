# import urllib.request
# response = urllib.request.urlopen(url='http://www.baidu.com/')
# html = response.read().decode('utf-8')
# print(html)
#
# # 返回实际数据的url地址
# url = response.geturl()
# # http 响应码
# code = response.getcode()
# print(url, code)

from urllib import parse
params = {
    'ie':'utf-8',
    'wd':'美女'
}
params_str = parse.urlencode(params)
url = 'https://www.baidu.com/s?'+params_str
print(url)

url = 'https://www.baidu.com/s?%s'%params_str
print(url)
url = 'https://www.baidu.com/s?{}'.format(params_str)
print(url)

url = 'https://www.baidu.com/s?{}'
params = 'ie=utf-8&wd=%E7%BE%8E%E5%A5%B3'
url = url.format(params)


# 抓取贴吧数据

from urllib import request, parse
import time, random

class BaiduSpider():
    def __init__(self):
        self.url = 'https://tieba.baidu.com/f?kw={}&ie=utf-8&pn={}'

    def get_html(self, url):
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36'}
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
        params = parse.quote(name)
        for page in range(begin, end+1):
            pn = (page-1)*50
            filename = '{}-第{}页.html'.format(name, page)
            url = self.url.format(params, pn)
            html = self.get_html(url)
            self.save_html(filename, html)
            time.sleep(random.randint(1, 3))

if __name__ == '__main__':
    start = time.time()
    spider = BaiduSpider()
    spider.run()
    end = time.time()
    print('执行时间%.2f' % (end-start))
