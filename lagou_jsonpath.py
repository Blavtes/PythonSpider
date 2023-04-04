import requests,jsonpath,json
from fake_useragent import UserAgent

url = 'https://www.lagou.com/lbs/getAllCitySearchLabels.json'
us = UserAgent()
headers = {
    'User-Agent':us.random
}
res = requests.get(url=url,headers=headers)
html_str = res.content.decode()
#把json格式转换成py格式
html_py = json.loads(html_str)
print(html_py)
# 从根节点开始获取key的name
#jsonpatch中用法
#$ 根节点 . 子节点 .. 所有符合的节点
city_list = jsonpath.jsonpath(html_py,'$..name')
print(city_list)

