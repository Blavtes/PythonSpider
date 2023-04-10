# 1、创建爬虫目录
# scrapy startproject 项目名
# 2、创建爬虫文件
# scrapy genspider 爬虫名 域名
# 3、运行爬虫
# scrapy crawl 爬虫名

#settings.py
# 修改全局配置
# ROBOTSTXT_OBEY = False
# 添加日志权限
# LOG_LEVEL = 'WARNING' 3
"""
# LOG_LEVEL = 'CRITICAL' 5 严重错误
# LOG_LEVEL = 'ERRO'     4 普通错误
# LOG_LEVEL = 'WARNING'  3 警告
# LOG_LEVEL = 'INFO'     2 一般信息
# LOG_LEVEL = 'DEBUG'    1 调试信息
"""
import scrapy
# 启用管道
# ITEM_PIPELINES = {
#    'Bqg.pipelines.BqgPipeline': 300,
# }

# 解析文件中 item的key 一定要与items.py中的命名一致
# class BqgItem(scrapy.Item):
#     # define the fields for your item here like:
#     # 对应要爬取的内容
#     name = scrapy.Field()
#     url = scrapy.Field()


# 运行文件 新建与scrapy.py同级文件
# from scrapy import cmdline
# cmdline.execute('scrapy crawl baidu'.split())

# 持久化 mysql
# 1、在setting.py 中定义相关变量
# 2、pipelines.py中导入settings模块
#     def open_spider(self,spider):
#             链接数据库
#     def close_spider(self,spider):
#             关闭数据库
# 3、settings.py中添加此管道
#     ITEM_PIPELINES={":200}
#

# 数据库相关变量
# MYSQL_HOST = '127.0.0.1'
# MYSQL_USER = 'root'
# MYSQL_PWD = 'YYyangyong00'
# MYSQL_DB = 'xiaomi'
# MYSQL_CHAR = 'utf8'

# ITEM_PIPELINES = {
#    'Xiaomi_thread.pipelines.XiaomiThreadPipeline': 300,
#    'Xiaomi_thread.pipelines.Xiaomi_MysqlPipeline':500
# }

# csv
# 命令行直接输出
# cmdline.execute('scrapy crawl xiaomi -o xiaomi.csv'.split())

# json
# 命令行直接输出
# cmdline.execute('scrapy crawl xiaomi -o xiaomi.json'.split())
# settings.py 设置编码
# FEED_EXPORT_ENCODING= 'utf-8' # 保存编码
# 非结构化数据存储路径
# IMAGES_STORE = '路径'
# 并发数
# CONCURRENT_REQUESTS= 32
# 间隔
# DOWNLOAD_DELAY = 3
# 下载器中间件
# DOWNLOADER_MIDDLEWARES = {}

# response 属性
# 1、response.text 获取响应内容-字符串
# 2、response.body 获取bytes数据类型
# 3、response.xpath('')
#
# response.xpath('')调用方法
# 1、结果：列表，元素为选择器对象
# <selector xpath='//article' data=''>
# 2、.extract() : 提取文本内容，将列表中的所有元素序列化为unicode字符串
# 3、.extract_first(): 提前列表中的第一个文本内容
# 4、.get() : 提取列表中的第一个文本内容 # python3.5 之后可用

# 中间件设置代理、user-agent、重写pipeline

# 分布式爬取数据配置 方式1、中型数据爬取
# 1、安装pip install scrapy_redis
# 1、使用scrapy_redis的调度器
# SCHEDULER = "scrapy_redis.scheduler.Scheduler"
# 2、使用scrapy_redis的去重机制
# DUPEFILTER_CLASS= "scrapy_redis.dupefilter.REPDupeFilter"
# 3、是否清除请求指纹，True不清除。False清除（默认）
# SCHEDULER_PERSIST = True
# 4、（非必须）在ITEM_PIPELINES中添加redis管道优先级（不添加，item数据不会添加redis数据库中）
# 'scrapy_redis.popelines.RedisPipeline' : 200
# 5、定义redis主机地址和端口号
# REDIS_HOST = '127.0.0.1'
# REDIS_PORT = 6379

# 方式2
# 1、不添加redis管道
# 2、在spider中引用
# from scrapy_redis.spider import RedisSpider
# 3、修改scrapy.Spider继承RedisSpider
# class TencentSpider(RedisSpider):
    # 去掉start_urls
    # 定义redis_key
    # redis_key = 'xxxx:spider'
    # 重写
   # def make_requsets_from_url(self,url):
   #     return scrapy.Request(url=url,dont_filter=True) #dont_filter 跨域

# 分布式运行程序后、需在redis数据库终端中执行
   # lpush redis_key start_url