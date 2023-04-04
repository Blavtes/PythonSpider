# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class XiaomiThreadPipeline:
    def process_item(self, item, spider):
        print(item['name'],item['two_url'])
        return item

import pymysql
from .settings import *
#自定义管道
class Xiaomi_MysqlPipeline:
    # 爬虫项目开始时 运行的函数
    def open_spider(self,spider):
        print('open_spider run ...')
        # 用于创建数据库连接
        self.db = pymysql.connect(
            host=MYSQL_HOST,
            user=MYSQL_USER,
            password=MYSQL_PWD,
            database=MYSQL_DB,
            charset=MYSQL_CHAR
        )
        self.cursor = self.db.cursor() # 游标
    # 每一个管道类都要有一个process_item函数来承接
    def process_item(self,item,spider):
        ins = 'insert into apptab values(%s,%s,%s)'
        L = [
            item['name'],item['two_url'],item['down_url']
        ]
        self.cursor.execute(ins,L)
        self.db.commit()
        # 管道中有可能有多个item 所以必须返回
        return item
    # 爬虫结束时 运行的函数
    def close_spider(self,spider):
        print('close_spider....')
        self.cursor.close()
        self.db.close()
