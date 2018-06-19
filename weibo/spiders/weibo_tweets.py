# -*- coding: utf-8 -*-
from scrapy import Spider, Request, FormRequest
import scrapy
from scrapy.selector import Selector
import json
import demjson
import datetime
import logging as log
from weibo.items import InformationItem, TweetsItem, TestItem


class WeiboTweetsSpider(scrapy.Spider):
    name = 'weibo_tweets'
    allowed_domains = ['m.weibo.com']
    start_urls = ['http://m.weibo.com/']

    start_url = 'https://m.weibo.cn/api/container/getSecond?containerid={include}'
    start_url_next = 'https://m.weibo.cn/api/container/getSecond?containerid={include}&page={j}'
    start_include = '1005053905389155_-_FOLLOWERS'
    # start
    start_profile_url = 'https://m.weibo.cn/api/container/getIndex?uid={weiboid}&luicode=10000012&lfid={include}&containerid=107603{weiboid}'
    start_profile_url_next = 'https://m.weibo.cn/api/container/getIndex?uid={weiboid}&luicode=10000012&lfid={include}&containerid=107603{weiboid}&page={j}'
    # start_profile
    followers_profile_url = 'https://m.weibo.cn/api/container/getIndex?uid={weiboid}&luicode=10000011&lfid=231051_-_followers_-_{last_id}&type=uid&value={weiboid}&containerid=107603{weiboid}'

    # def start_requests(self):
    #     yield Request(self.start_url.format(include=self.start_include),self.parse_user,dont_filter=True)
    #     for i in range(2, 6):
    #         count = i
    #         yield Request(self.start_url_next.format(include=self.start_include, j=count), self.parse_user,dont_filter=True)
    #     #开始页进行爬取

    def start_requests(self):
        yield Request(self.start_profile_url.format(weiboid='1749127163', include=self.start_include),
                      self.parse_homepage, dont_filter=True)

    def parse_homepage(self, response):
        now = datetime.datetime.now()
        # json_homepage = demjson.decode(response.body_as_unicode())
        json_homepage = json.loads(response.body_as_unicode())
        tweetsitem = TweetsItem()
        # tweetsitem['id'] = json_homepage['data']['cardlistInfo']['containerid'][6:]
        if json_homepage['data']['cards']:
            count = -1
            for i in json_homepage['data']['cards']:
                count += 1
            for i in range(count):
                if json_homepage['data']['cards'][i]['card_type'] == 9:
                    tweetsitem['id'] = json_homepage['data']['cards'][i]['mblog']['user']['id']
                    tweetsitem['spider_time'] = now.strftime('%Y/%m/%d %H:%M:%S')
                    tweetsitem['screen_name'] = json_homepage['data']['cards'][i]['mblog']['user']['screen_name']
                    tweetsitem['text'] = json_homepage['data']['cards'][i]['mblog']['text']
                    tweetsitem['created_at'] = json_homepage['data']['cards'][i]['mblog']['created_at']
                    tweetsitem['comments_count'] = json_homepage['data']['cards'][i]['mblog']['comments_count']
                    tweetsitem['isLongText'] = json_homepage['data']['cards'][i]['mblog']['isLongText']
                    tweetsitem['is_paid'] = json_homepage['data']['cards'][i]['mblog']['is_paid']
                    tweetsitem['attitudes_count'] = json_homepage['data']['cards'][i]['mblog']['attitudes_count']
                    tweetsitem['mblog_id']=json_homepage['data']['cards'][i]['mblog']['mid']
                    if json_homepage['data']['cards'][i]['mblog']['source'] is not None:
                        tweetsitem['source'] = json_homepage['data']['cards'][i]['mblog']['source']
                    try:
                        tweetsitem['retweeted_status'] = json_homepage['data']['cards'][i]['mblog']['retweeted_status']
                    except Exception as e:
                        log.info('no retweeted_status')
                    #tweetsitem['_id'] = tweetsitem.created_Id()
                    yield tweetsitem
            if 'page' in response.url:
                page = response.url.split("page=")[-1]

                yield Request(
                    self.start_profile_url_next.format(weiboid='1749127163', include=self.start_include,
                                                       j=int(page) + 1),
                    self.parse_homepage, dont_filter=True)
            else:
                yield Request(
                    self.start_profile_url_next.format(weiboid='1749127163', include=self.start_include,
                                                       j=2),
                    self.parse_homepage, dont_filter=True)

