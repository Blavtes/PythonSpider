from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver import ChromeOptions
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from fake_useragent import UserAgent
import time
# //*[@id="listAll"]/section[2]/div[2]/ul/li/div/a/div[2]/div[1]/h3 名字
# //*[@id="listAll"]/section[2]/div[2]/ul/li/div/a/div[2]/div[1]/span 类型
# //*[@id="listAll"]/section[2]/div[2]/ul/li/div/a/div[2]/div[2]/h2/div 作者
# //*[@id="listAll"]/section[2]/div[2]/div/ul/li[9]/span 作者

class DouYuSpider():
    def __init__(self):
        self.url = 'https://www.douyu.com/directory/all'
        self.driver = webdriver.Chrome()

    def parse_data(self):
        time.sleep(20)
        room_list = self.driver.find_elements(by=By.XPATH,value='//*[@id="listAll"]/section[2]/div[2]/ul/li/div')
        print(len(room_list))
        data_list = []
        for room in room_list:
            tem = {}
            tem['title'] = room.find_element(by=By.XPATH,value='./a/div[2]/div[1]/h3').text
            tem['type'] = room.find_element(by=By.XPATH,value='./a/div[2]/div[1]/span').text
            tem['owner'] = room.find_element(by=By.XPATH,value='./a/div[2]/div[2]/h2/div').text
            data_list.append(tem)
        return data_list,len(room_list)

    def save_data(self,data_list):
        for data in data_list:
            print(data)

    def run(self):
        number = 0
        self.driver.get(self.url)
        while True:
            data_list,num = self.parse_data()
            self.save_data(data_list)
            if num < 120:
                break
            try:
                self.driver.execute_script('scrollTo(0,10000000000)')
                el_next = self.driver.find_element(by=By.XPATH,value='//*[@id="listAll"]/section[2]/div[2]/div/ul/li[9]/span|//*[@id="listAll"]/section[2]/div[2]/div/ul/li[10]/span|//*[@id="listAll"]/section[2]/div[2]/div/ul/li[11]/span')

                el_next.click()
                number += 1
                print('第%d爬取完成'%(number))
            except Exception as e:
                print(e)

if __name__ == '__main__':
    douyu = DouYuSpider()
    douyu.run()

