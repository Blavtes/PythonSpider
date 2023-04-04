import re
import requests, time, random
from lxml import etree
from fake_useragent import UserAgent

class GetProxyIp():
    def __init__(self):
        self.url = 'https://www.89ip.cn/index_{}.html'
    def get_headers(self):
        ua = UserAgent()
        headers = {'User-Agent':ua.random}
        return headers
    def get_ip_file(self,url):
        html = requests.get(url=url,headers=self.get_headers(),timeout=5).text
        parse_html = etree.HTML(html)
        tr_list = parse_html.xpath('//tr')
        for tr in tr_list[1:]:
            ip = tr.xpath('./td[1]/text()')[0].strip()
            port = tr.xpath('./td[2]/text()')[0].strip()
            self.test_ip(ip,port)
    def test_ip(self,ip,port):
        proxies={
            'http':'http://{}:{}'.format(ip,port),
            'https': 'https://{}:{}'.format(ip, port),
        }
        test_url = 'http://httpbin.org/get'
        statis = ''
        try:
            res=requests.get(url=test_url,headers=self.get_headers(),proxies=proxies,timeout=8)
            print(res.text,res.status_code)
            if res.status_code == 200:
                print(ip,port,'sussce')
                if not self.if_touming(res.text):

                    with open('./proxies.txt','a') as f:
                        f.write(ip+':'+port+'\n')
                else:
                    print('透明的========')
                    print(res.text)
        except Exception as e:
            print(ip,port,'Failed')
    # 判断是否透明，是否包含本机外网ip http://whatismyip.com
    def if_touming(self,html):
        parse_html = re.compile('116.25.40.13',re.S)
        r_list = parse_html.findall(html)
        if r_list:
            return True
        else:
            return False

    def run(self):
        for i in range(1,100):
            url=self.url.format(i)
            self.get_ip_file(url)
            time.sleep(random.randint(5,10))
if __name__ == '__main__':
    getIp = GetProxyIp()
    getIp.run()