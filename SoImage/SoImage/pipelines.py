# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import scrapy
# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

from scrapy.pipelines.images import ImagesPipeline
# 重写 ImagesPipeline
class SoimagePipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        print(item['img_title'])
        yield scrapy.Request(
           url= item['img_link'],
            meta = {'title':item['img_title']}
        )

    def file_path(self, request, response=None, info=None, *, item=None):
        filename = request.meta['title'] +'.'+request.url.split('.')[-1]
        return filename