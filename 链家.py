import requests, time, random,csv
from lxml import etree
from fake_useragent import UserAgent

class LianjiaSpider():
    def __init__(self):
        self.url = 'https://sz.lianjia.com/ershoufang/pg{}/'
        self.number = 1
    # 得到页面
    def get_html(self,url):
        ua = UserAgent();
        headers = {'User-Agent':ua.random}
        # 尝试3次不通就换下一个
        if self.number <= 3 :
            try:
                res = requests.get(url,headers,timeout=5)
                res.encoding='utf-8'
                html=res.text
                self.parse_page(html)
                self.number = 1
            except Exception as e:
                print('Retry',self.number,e)
                self.number += 1
                self.get_html(url)
    # 解析
    def parse_page(self,html):
        # 创建解析对象
        parse_html = etree.HTML(html)
        xp_dbs = '//ul[@class="sellListContent"]/li[@class="clear LOGVIEWDATA LOGCLICKDATA"]'
        li_list = parse_html.xpath(xp_dbs)
        # 存储到csv 中，必须要用list套元组的格式
        item = {}
        L = []
        i = 1
        for li in li_list:
            # 名称
            xp_name = './/div[@class="title"]/a/text()'
            name_list = li.xpath(xp_name)
            # 如果不存在就置为空
            item['name'] = name_list[0].strip() if name_list else None
            # 小区名
            xpath_positionInfo= '//li//div[@class="positionInfo"]/a/text()'
            positionInfo_list = parse_html.xpath(xpath_positionInfo)
            item['positionInfo'] = positionInfo_list[0] if positionInfo_list else None
            # 房屋信息
            # houseInfo
            xpath_houseInfo = '//li//div[@class="houseInfo"]/text()'
            houseInfo_list = parse_html.xpath(xpath_houseInfo)
            if houseInfo_list:
                info_arr = houseInfo_list[0].split('|')
                if len(info_arr) == 7:
                    item['model'] = info_arr[0].strip() #户型
                    item['area'] = info_arr[1].strip() #面积
                    item['direction'] = info_arr[2].strip() #朝向
                    item['zhuangxiu'] = info_arr[3].strip() #
                    item['floor'] = info_arr[4].strip()
                    item['crateTime'] = info_arr[5].strip()
                    item['floorType'] = info_arr[6].strip()
                else:
                    item['model'] = item['area'] = item['direction'] = item['zhuangxiu'] = item['floor'] = item['crateTime'] = item['floorType'] = None
            else:
                item['model'] = item['area'] = item['direction'] = item['zhuangxiu'] = item['floor'] = item['crateTime'] = item['floorType'] = None
            # 总价 priceInfo
            xpath_totalPrice= '//li//div[@class="totalPrice totalPrice2"]/span/text()'
            totalPrice_list = parse_html.xpath(xpath_totalPrice)
            item['totalPrice'] = totalPrice_list[0].strip() if totalPrice_list else None
            # 单价 95,306元/平
            xpath_unitPrice = '//li//div[@class="unitPrice"]/span/text()'
            unitPrice_list = parse_html.xpath(xpath_unitPrice)
            item['unitPrice'] = unitPrice_list[0].strip()[:-3] if unitPrice_list else None
            print(i,item)
            i += 1
            L.append((item['name'],item['positionInfo'],item['model'] , item['area'],
                      item['direction'],item['zhuangxiu'], item['floor'], item['crateTime'],
                      item['floorType'],item['totalPrice'],item['unitPrice']))
        self.save_data(L)
    def save_data(self,L):
        with open('lianjia.csv','a',newline='',encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerows(L)
    def run(self):
        for pg in range(1, 3):
            self.number = 1
            url = self.url.format(pg)
            self.get_html(url)
            time.sleep(random.randint(1,3))
if __name__ == '__main__':
    sprider = LianjiaSpider()
    sprider.run()