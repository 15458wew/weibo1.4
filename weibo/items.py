# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Field


class InformationItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    table_name='weibo_users_information'

    screen_name = Field()
    id = Field()
    cover_image_phone=Field()
    close_blue_v=Field()
    desc1=Field()
    desc2=Field()
    description=Field()
    follow_count=Field()
    followers_count=Field()
    gender=Field()
    profile_url=Field()
    verified_reason=Field()
    spider_time=Field()
    url=Field()
    verified=Field()

class TweetsItem(scrapy.Item):
    table_name='weibo_tweets'
    mblog_id = Field()
    screen_name=Field()
    id=Field()
    created_at = Field()
    text = Field()
    attitudes_count = Field()
    comments_count=Field()
    source=Field()
    isLongText=Field()
    is_paid=Field()
    spider_time=Field()
    is_top=Field()
    retweeted_status=Field()
    ve=Field()


class TestItem(scrapy.Item):
    table_name='test_id'
    id=Field()


