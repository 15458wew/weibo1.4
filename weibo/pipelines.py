# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from weibo.items import TweetsItem,InformationItem

class MongoPipeline(object):
    collection_name='users'

    def __init__(self,mongo_host,mongo_port,mongo_db):
        self.mongo_host=mongo_host
        self.mongo_port=mongo_port
        self.mongo_db=mongo_db

    @classmethod
    def from_crawler(cls,crawler):
        return cls(
            mongo_host=crawler.settings.get('MONGO_HOST'),
            mongo_port=crawler.settings.get('MONGO_PORT'),
            mongo_db=crawler.settings.get('MONGO_DB')
        )

    def open_spider(self,spider):
        self.client=pymongo.MongoClient(host=self.mongo_host,port=self.mongo_port)
        self.db=self.client[self.mongo_db]

    def close_spider(self,spider):
        self.client.close()

    def process_item(self,item,spider):
        # self.db[item.table_name].update({'id':item.get('id')},{'$set':dict(item)},True)

        collection = self.db[item.table_name]
        if item.table_name =='weibo_tweets' and item.get('ve') == True:
            collection.update({'mblog_id':item.get('mblog_id')},{'$set':dict(item)},True)
        elif  item.table_name=='weibo_users_information' and item.get('verified') == True:
            collection.update({'id':item.get('id')},{'$set':dict(item)},True)
            #collection.save(dict(item))

        return item
