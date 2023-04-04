import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC #设置要定位的标签
from fake_useragent import UserAgent
def noscreen():
#实现无界面浏览器
    chrome_options = Options()
    # chrome_options.add_argument('--headless')
    # chrome_options.add_argument('--disable-gpu')
    # 提示
    option = ChromeOptions()
    option.add_experimental_option('excludeSwitches',['enable-automation'])
    driver = webdriver.Chrome(chrome_options=chrome_options,options=option) # ,executable_path='驱动相对路径')
    driver.get('http://www.baidu.com')

    #把网页保存成图片
    driver.save_screenshot('baidu.png')
    #资源释放
    driver.page_source
    print(driver.title)
    time.sleep(2)
    driver.find_element(by=By.ID,value='kw').send_keys('python')
    time.sleep(2)
    driver.find_element(by=By.XPATH,value='//*[@class="bg s_btn"]').click()
    time.sleep(10)
    driver.find_element(by=By.ID,value='kw').send_keys('python')
    time.sleep(10)
    # driver.find_element(by=By.ID,value='s1').click()
    # time.sleep(10)
    driver.find_element(by=By.ID,value='kw').send_keys('32323')
    # time.sleep(10)
    driver.find_element(by=By.LINK_TEXT,value='hao123').click()
    #包含链接字段
    driver.find_element(by=By.PARTIAL_LINK_TEXT,value='123').click()
    driver.find_element(by=By.CLASS_NAME,value='c-icon quickdelete c-color-gray2').click()

def find_elements():
    driver.get('https://www.dapengjiaoyu.cn/square')
    res = driver.find_elements(by=By.TAG_NAME,value='ul')
    print(res)
    res = driver.find_elements(by=By.LINK_TEXT,value='推荐')
    print(res[0].get_attribute('href')) # 不用s 就不是列表
    res = driver.find_element(by=By.LINK_TEXT,value='作业')
    print(res.get_attribute('href'))
    driver.get('https://sz.58.com/ershoufang/?PGTID=0d200001-0000-4f6f-cd94-9f188b5d40b6&ClickID=1')
    time.sleep(2)
    a_list = driver.find_elements(by=By.XPATH,value='//*[@id="__layout"]/div/section/section[3]/section[1]/section[2]/div/a')
    for a in a_list:
        print(a.text)
        print(a.get_attribute('href'))
    driver.quit()
    # 窗口句柄

def checkoutwindos():
    driver.get('http://www.baidu.com')
    time.sleep(2)
    driver.find_element(by=By.ID,value='kw').send_keys('python')
    driver.find_element(by=By.ID,value='su').click()
    time.sleep(2)
    js = 'window.open("https://www.sogou.com")'
    driver.execute_script(js)
    time.sleep(2)
    # 获取所有的窗口
    windos = driver.window_handles
    time.sleep(2)
    # 切换窗口
    driver.switch_to.window(windos[0])
    time.sleep(2)
    driver.switch_to.window(windos[1])

    # '//dd[@id="secitem-type"]/a[@class="select"]'
    # driver.get('https://sz.58.com/hezu/?PGTID=0d3090a7-0000-479a-3e3f-8703afa7949d&ClickID=4')
    # time.sleep(2)
    # driver.find_element(by=By.XPATH,value='//dd[@id="secitem-type"]/a[@class="select"]').click()
    driver.quit()
def qqquezLogin():
    # qq 空间登录
    url = 'https://i.qq.com'
    driver.get(url)
    time.sleep(10)
    # 找到登录iframe
    iframe = driver.find_element(by=By.XPATH,value='//*[@id="login_frame"]')
    driver.switch_to.frame(iframe)
    # 切换登录
    driver.find_element(by=By.XPATH,value='//*[@id="switcher_plogin"]').click()
    time.sleep(2)
    driver.find_element(by=By.XPATH,value='//*[@id="u"]').send_keys('574949555')
    # time.sleep(2)
    driver.find_element(by=By.ID,value='p').send_keys('---?-')
    driver.find_element(by=By.ID,value='login_button').click()
    time.sleep(20)
    driver.quit()

def delet_cookie():
    url = 'https://www.baidu.com'
    driver.get(url)
    print(driver.get_cookies())
    cookies = {data['name']:data['value'] for data in driver.get_cookies()}
    print(cookies)
    driver.delete_cookie('BAIDUID_BFESS')
    cookies = {data['name']:data['value'] for data in driver.get_cookies()}
    print(cookies)

#滚动距离
def scriptjs():
    driver.get('https://www.dapengjiaoyu.cn/')
    time.sleep(3)
    js = 'window.scrollTo(0,document.body.scrollHeight)'
    driver.execute_script(js)
    time.sleep(5)
    driver.quit()

def scrollwindow():
    driver.get('https://www.toutiao.com/?wid=1680077558749')
    # 强制等待
    time.sleep(5)
    js = 'scrollTo(0,1300)'
    driver.execute_script(js)
    driver.find_element(by=By.XPATH,value='//div[@class="video-item"][5]/div[@class="right-content"]/a[@class="title"]').click()
    time.sleep(10)


def hidewaite():
    driver.get('https://www.baidu.com')
    # 隐式等待
    driver.implicitly_wait(20)
    print('ok')
    driver.find_element(by=By.XPATH,value='//a[@class="title-content c-link c-font-medium c-line-clamp1"]/span[@class="title-content-title"]').click()
    # time.sleep(10)
    # 显示等待
    WebDriverWait(driver,20,0.5).until(EC.presence_of_element_located((By.LINK_TEXT,'hao123')))
    # 参数20表示最长等时间
    # 0.5为没0.5s查一次标签是否存在
    # EC.presence_of_element_located((By.LINK_TEXT,'hao123') 标签定位
    # 20s 结束不存在抛异常
    print(driver.find_element(by=By.LINK_TEXT,value='hao123').get_attribute('href'))

def taobao():
    driver.get('http://www.taobao.com')
    time.sleep(1)
    for i in range(10):
        try:
            driver.implicitly_wait(3)
            element = driver.find_element(by=By.XPATH,value='//div[@class="tb-footer-hd"]/p/span[7]/a')
            print(element.get_attribute('href'))
            break
        except:
            js = 'window.scrollTo(0,{})'.format(i*500)
            driver.execute_script(js)
            print(i)

def notinterface():

    opt = webdriver.ChromeOptions()
    opt.add_argument('--headless')
    # opt.add_argument('--disable-gpu')
    driver = webdriver.Chrome(chrome_options=opt)
    driver.get('http://www.taobao.com')
    time.sleep(1)
    for i in range(10):
        try:
            WebDriverWait(driver,10,0.5).until(
                EC.presence_of_element_located((By.XPATH,'//div[@class="tb-footer-hd"]/p/span[7]/a'))
            )
            element = driver.find_element(by=By.XPATH,value='//div[@class="tb-footer-hd"]/p/span[7]/a')
            print(element.get_attribute('href'))
        except:
            js = 'window.scrollTo(0,{})'.format(i * 500)
            driver.execute_script(js)
            print(i)

def ipageent():
    opt = webdriver.ChromeOptions()
    opt.add_argument('--proxy-server=http://222.190.223.181:8089')
    driver = webdriver.Chrome(chrome_options=opt)
    driver.get('http://httpbin.org/get')
    print(driver.page_source)

#修改代理
def useragent():
    ua = UserAgent()
    opt = webdriver.ChromeOptions()
    # 添加的useragent格式不对就会返回真实的useragent
    opt.add_argument('--user-agent='+ua.random)
    driver = webdriver.Chrome(chrome_options=opt)
    driver.get('http://httpbin.org/get')
    print(driver.page_source)
    #
#斗鱼
def douyu():
    url = 'https://www.douyu.com/directory/all'



if __name__=="__main__":
    driver = webdriver.Chrome()
    # delet_cookie()
    # hidewaite()
    douyu()