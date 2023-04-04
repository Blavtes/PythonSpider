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