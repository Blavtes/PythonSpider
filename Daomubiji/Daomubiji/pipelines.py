# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

import os
class DaomubijiPipeline:
    def process_item(self, item, spider):
        # 每一部小说创建一个目录
        # 返回的章节无序，不能直接追加存储到txt
        dir = '{}/'.format(item['title'])
        if not os.path.exists(dir):
            os.mkdir(dir)
        filename = dir + item['name'] + '.txt'
        with open(filename,'w',encoding='utf-8') as f:
            f.write(item['content'])
        return item
