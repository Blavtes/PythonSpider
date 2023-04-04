from selenium import webdriver
from selenium.webdriver import ChromeOptions
import time
#配置谷歌浏览器
option = ChromeOptions()
# option.add_experimental_option('useAutomationExtension',False)
#提示
option.add_experimental_option('excludeSwitches',['enable-automation'])

#创建驱动对象
driver = webdriver.Chrome(options=option)
driver.get('http://www.baidu.com')
time.sleep(10)
print(driver.title)
#关闭对象
driver.quit()