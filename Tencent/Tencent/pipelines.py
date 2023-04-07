# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class TencentPipeline:
    def process_item(self, item, spider):
        print(item['job_name'])
        return item

import pymysql
from .settings import *
class TTMPipeline:
    def open_sipder(self,spider):
        self.db = pymysql.connect(
            host= MYSQL_HOST,
            user=MYSQL_USER,
            password=MYSQL_PWD,
            database=MYSQL_DB,
            charset=MYSQL_CHAR
        )
        self.cursor = self.db.cursor()
    def process_item(self,item,spider):
        ins = 'insert into tencenttab values(%s,%s,%s,%s,%s,%s)'
        L = [
            item['job_name'],
            item['job_CategoryName'],
            item['job_Responsibility'],
            item['job_Requirement'],
            item['job_LocationName'],
            item['job_LastUpdateTime'],
        ]
        self.cursor.execute(ins,L)
        self.db.commit()
        return item
    def close_spider(self,spider):
        self.cursor.close()
        self.db.close()