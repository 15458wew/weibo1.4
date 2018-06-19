# -*- coding: utf-8 -*-
from scrapy import Spider, Request, FormRequest
import scrapy
from scrapy.selector import Selector
import json

import logging as log
from weibo.items import InformationItem, TweetsItem
import datetime

class WeiboUserSpider(scrapy.Spider):
    name = 'weibo_user2'
    allowed_domains = ['m.weibo.com']
    start_urls = ['http://m.weibo.com/']

    start_url = 'https://m.weibo.cn/api/container/getSecond?containerid={include}'
    start_url_next = 'https://m.weibo.cn/api/container/getSecond?containerid={include}&page={j}'
    start_include = '1005053905389155_-_FOLLOWERS'
    # start_url and start_url_next

    followers_url = 'https://m.weibo.cn/api/container/getIndex?containerid=231051_-_followers_-_{weiboid}&featurecode=2000320'
    followers_url_next = 'https://m.weibo.cn/api/container/getIndex?containerid=231051_-_followers_-_{weiboid}&featurecode=2000320&page={j}'
    # followers_url and followers_url_next

    fans_url = 'https://m.weibo.cn/api/container/getIndex?containerid=231051_-_fans_-_{weiboid}&featurecode=2000320'
    fans_url_next = 'https://m.weibo.cn/api/container/getIndex?containerid=231051_-_fans_-_{weiboid}&featurecode=2000320&since_id={j}'
    # fans_url and fans_url_next

    #========================个人微博内容爬取项=============

    start_profile_url = 'https://m.weibo.cn/api/container/getIndex?uid={weiboid}&luicode=10000012&lfid={include}&containerid=107603{weiboid}'
    start_profile_url_next = 'https://m.weibo.cn/api/container/getIndex?uid={weiboid}&luicode=10000012&lfid={include}&containerid=107603{weiboid}&page={j}'
    # start_profile

    followers_profile_url='https://m.weibo.cn/api/container/getIndex?uid={weiboid}&luicode=10000012&lfid=231051_-_follow_-_{last_id}&type=uid&value={weiboid}&containerid=107603{weiboid}'
    followers_profile_url_next='https://m.weibo.cn/api/container/getIndex?uid={weiboid}&luicode=10000012&lfid=231051_-_follow_-_{last_id}&type=uid&value={weiboid}&containerid=107603{weiboid}&page={j}'
    #followers_profile

    fans_profile_url='https://m.weibo.cn/api/container/getIndex?uid={weiboid}&luicode=10000011&lfid=231051_-_fans_-_{last_id}&featurecode=20000320&type=uid&value={weiboid}&containerid=107603{weiboid}'
    fans_profile_url_next='https://m.weibo.cn/api/container/getIndex?uid={weiboid}&luicode=10000011&lfid=231051_-_fans_-_{last_id}&featurecode=20000320&type=uid&value={weiboid}&containerid=107603{weiboid}&page={j}'
    #fans_profile

    def start_requests(self):
        yield Request(self.start_url.format(include=self.start_include), self.parse_user)
        for i in range(1, 6):
            count = i
            yield Request(self.start_url_next.format(include=self.start_include, j=count), self.parse_user)
        #开始页进行爬取

    def parse_user(self, response):
        now=datetime.datetime.now()
        json_object = json.loads(response.body_as_unicode())
        weiboItem = InformationItem()
        count = -1
        for i in json_object['data']['cards']:
            count += 1
        for i in range(count):
            weiboItem['screen_name'] = json_object['data']['cards'][i]['user']['screen_name']
            weiboItem['description'] = json_object['data']['cards'][i]['user']['description']
            weiboItem['follow_count'] = json_object['data']['cards'][i]['user']['follow_count']
            weiboItem['followers_count'] = json_object['data']['cards'][i]['user']['followers_count']
            weiboItem['gender'] = json_object['data']['cards'][i]['user']['gender']
            weiboItem['id'] = json_object['data']['cards'][i]['user']['id']
            weiboItem['profile_url'] = json_object['data']['cards'][i]['user']['profile_url']
            weiboItem['close_blue_v'] = json_object['data']['cards'][i]['user']['close_blue_v']
            weiboItem['desc1'] = json_object['data']['cards'][i]['user']['desc1']
            weiboItem['desc2'] = json_object['data']['cards'][i]['user']['desc2']
            weiboItem['cover_image_phone'] = json_object['data']['cards'][i]['user']['cover_image_phone']
            weiboItem['spider_time']=now.strftime('%Y/%m/%d %H:%M:%S')
            if json_object['data']['cards'][i]['user']['verified'] == True:
                weiboItem['verified_reason'] = json_object['data']['cards'][i]['user']['verified_reason']
            else:
                weiboItem['verified_reason'] = None
            yield Request(self.followers_url.format(weiboid=weiboItem['id']), self.parse_followers,dont_filter=True)
            yield Request(self.fans_url.format(weiboid=weiboItem['id']),self.parse_fans,dont_filter=True)
            yield Request(self.start_profile_url.format(weiboid=weiboItem['id'],include=self.start_include),self.parse_homepage,dont_filter=True)
            yield weiboItem
            #爬取开始页的用户信息，并将用户的关注粉丝列表传递下一项

    def parse_followers(self, response):
        now = datetime.datetime.now()
        json_object = json.loads(response.body_as_unicode())
        weiboItem = InformationItem()
        try:
           last_id=json_object['data']['cardlistInfo']['containerid'][6:]
        except Exception as e:
            log.info('no cardlistInfo')
        if json_object['data']['cards']:
            count = -1
            for i in json_object['data']['cards'][0]['card_group']:
                count += 1
            for i in range(count):
                weiboItem['screen_name'] = json_object['data']['cards'][0]['card_group'][i]['user']['screen_name']
                weiboItem['description'] = json_object['data']['cards'][0]['card_group'][i]['user']['description']
                weiboItem['follow_count'] = json_object['data']['cards'][0]['card_group'][i]['user']['follow_count']
                weiboItem['followers_count'] = json_object['data']['cards'][0]['card_group'][i]['user']['followers_count']
                weiboItem['gender'] = json_object['data']['cards'][0]['card_group'][i]['user']['gender']
                weiboItem['id'] = json_object['data']['cards'][0]['card_group'][i]['user']['id']
                weiboItem['profile_url'] = json_object['data']['cards'][0]['card_group'][i]['user']['profile_url']
                weiboItem['close_blue_v'] = json_object['data']['cards'][0]['card_group'][i]['user']['close_blue_v']
                weiboItem['desc1'] = json_object['data']['cards'][0]['card_group'][i]['user']['desc1']
                weiboItem['desc2'] = json_object['data']['cards'][0]['card_group'][i]['user']['desc2']
                weiboItem['spider_time'] = now.strftime('%Y-%m-%d %H:%M:%S')
                weiboItem['cover_image_phone'] = json_object['data']['cards'][0]['card_group'][i]['user']['cover_image_phone']
                try:
                    if json_object['data']['cards'][0]['card_group'][i]['user']['verified'] == True:
                        weiboItem['verified_reason'] = json_object['data']['cards'][0]['card_group'][i]['user']['verified_reason']
                    else:
                        weiboItem['verified_reason'] = None
                except Exception as e:
                    log.info('verified is None')
                yield weiboItem
                yield Request(self.followers_url.format(weiboid=weiboItem['id']),self.parse_followers,dont_filter=True)
                yield Request(self.fans_url.format(weiboid=weiboItem['id']),self.parse_fans,dont_filter=True)

                yield Request(self.fans_profile_url.format(weiboid=weiboItem['id'],last_id=last_id),self.parse_homepage_for_followers_and_fans,dont_filter=True)
                yield Request(self.followers_profile_url.format(weiboid=weiboItem['id'],last_id=last_id),self.parse_homepage_for_followers_and_fans,dont_filter=True)

            if 'page' in response.url:
                page=response.url.split('page=')[-1]
                yield Request(self.followers_url_next.format(weiboid=weiboItem['id'], j=int(page)+1), self.parse_followers,dont_filter=True)
            else:
                yield Request(self.followers_url_next.format(weiboid=weiboItem['id'], j=2), self.parse_followers,dont_filter=True)
            #爬取所有的关注

    def parse_fans(self,response):
        now = datetime.datetime.now()
        json_object = json.loads(response.body_as_unicode())
        try:
           last_id=json_object['data']['cardlistInfo']['containerid'][6:]
        except Exception as e:
            log.info('no cardlistInfo')
        weiboItem = InformationItem()
        if json_object['data']['cards']:
            count = -1
            for i in json_object['data']['cards'][0]['card_group']:
                count += 1
            for i in range(count):
                weiboItem['screen_name'] = json_object['data']['cards'][0]['card_group'][i]['user']['screen_name']
                weiboItem['description'] = json_object['data']['cards'][0]['card_group'][i]['user']['description']
                weiboItem['follow_count'] = json_object['data']['cards'][0]['card_group'][i]['user']['follow_count']
                weiboItem['followers_count'] = json_object['data']['cards'][0]['card_group'][i]['user'][
                    'followers_count']
                weiboItem['gender'] = json_object['data']['cards'][0]['card_group'][i]['user']['gender']
                weiboItem['id'] = json_object['data']['cards'][0]['card_group'][i]['user']['id']
                weiboItem['profile_url'] = json_object['data']['cards'][0]['card_group'][i]['user']['profile_url']
                weiboItem['close_blue_v'] = json_object['data']['cards'][0]['card_group'][i]['user']['close_blue_v']
                weiboItem['desc1'] = json_object['data']['cards'][0]['card_group'][i]['user']['desc1']
                weiboItem['desc2'] = json_object['data']['cards'][0]['card_group'][i]['user']['desc2']
                weiboItem['cover_image_phone'] = json_object['data']['cards'][0]['card_group'][i]['user'][
                    'cover_image_phone']
                weiboItem['spider_time'] = now.strftime('%Y-%m-%d %H:%M:%S')
                try:
                    if json_object['data']['cards'][0]['card_group'][i]['user']['verified'] == True:
                        weiboItem['verified_reason'] = json_object['data']['cards'][0]['card_group'][i]['user'][
                            'verified_reason']
                    else:
                        weiboItem['verified_reason'] = None
                except Exception as e:
                    log.info('verified is None')
                yield weiboItem
                yield Request(self.fans_url.format(weiboid=weiboItem['id']), self.parse_fans,
                              dont_filter=True)
                yield Request(self.followers_url.format(weiboid=weiboItem['id']),self.parse_followers,dont_filter=True)

                yield Request(self.fans_profile_url.format(weiboid=weiboItem['id'], last_id=last_id),
                              self.parse_homepage_for_followers_and_fans, dont_filter=True)
                yield Request(self.followers_profile_url.format(weiboid=weiboItem['id'], last_id=last_id),
                              self.parse_homepage_for_followers_and_fans, dont_filter=True)

            if 'since_id' in response.url:
                since_id=response.url.split('since_id=')[-1]
                yield Request(self.fans_url_next.format(weiboid=weiboItem['id'], j=since_id),
                              self.parse_fans, dont_filter=True)
            else:
                yield Request(self.fans_url_next.format(weiboid=weiboItem['id'], j=2),
                              self.parse_fans, dont_filter=True)
    #爬取所有的粉丝
    #======================以下爬取微博内容=================>
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
                    tweetsitem['spider_time'] = now.strftime('%Y-%m-%d %H:%M:%S')
                    tweetsitem['screen_name'] = json_homepage['data']['cards'][i]['mblog']['user']['screen_name']
                    tweetsitem['text'] = json_homepage['data']['cards'][i]['mblog']['text']
                    tweetsitem['created_at'] = json_homepage['data']['cards'][i]['mblog']['created_at']
                    tweetsitem['comments_count'] = json_homepage['data']['cards'][i]['mblog']['comments_count']
                    tweetsitem['isLongText'] = json_homepage['data']['cards'][i]['mblog']['isLongText']
                    tweetsitem['is_paid'] = json_homepage['data']['cards'][i]['mblog']['is_paid']
                    tweetsitem['attitudes_count'] = json_homepage['data']['cards'][i]['mblog']['attitudes_count']
                    tweetsitem['mblog_id']=json_homepage['data']['cards'][i]['mblog']['id']
                    if json_homepage['data']['cards'][i]['mblog']['source'] is not None:
                        tweetsitem['source'] = json_homepage['data']['cards'][i]['mblog']['source']
                    try:
                        tweetsitem['retweeted_status'] = json_homepage['data']['cards'][i]['mblog']['retweeted_status']
                    except Exception as e:
                        log.info('no retweeted_status')
                    yield tweetsitem
            if 'page' in response.url:
                page = response.url.split("page=")[-1]

                yield Request(
                    self.start_profile_url_next.format(weiboid=tweetsitem['id'], include=self.start_include,
                                                       j=int(page) + 1),
                    self.parse_homepage, dont_filter=True)
            else:
                yield Request(
                    self.start_profile_url_next.format(weiboid=tweetsitem['id'], include=self.start_include,
                                                       j=2),
                    self.parse_homepage, dont_filter=True)

    def parse_homepage_for_followers_and_fans(self, response):
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
                    tweetsitem['spider_time'] = now.strftime('%Y-%m-%d %H:%M:%S')
                    tweetsitem['screen_name'] = json_homepage['data']['cards'][i]['mblog']['user']['screen_name']
                    tweetsitem['text'] = json_homepage['data']['cards'][i]['mblog']['text']
                    tweetsitem['created_at'] = json_homepage['data']['cards'][i]['mblog']['created_at']
                    tweetsitem['comments_count'] = json_homepage['data']['cards'][i]['mblog']['comments_count']
                    tweetsitem['isLongText'] = json_homepage['data']['cards'][i]['mblog']['isLongText']
                    tweetsitem['is_paid'] = json_homepage['data']['cards'][i]['mblog']['is_paid']
                    tweetsitem['mblog_id'] = json_homepage['data']['cards'][i]['mblog']['id']
                    tweetsitem['attitudes_count'] = json_homepage['data']['cards'][i]['mblog']['attitudes_count']
                    if json_homepage['data']['cards'][i]['mblog']['source'] is not None:
                        tweetsitem['source'] = json_homepage['data']['cards'][i]['mblog']['source']
                    try:
                        tweetsitem['retweeted_status'] = json_homepage['data']['cards'][i]['mblog']['retweeted_status']
                    except Exception as e:
                        log.info('no retweeted_status')
                    yield tweetsitem
            if 'page' in response.url:
                page = response.url.split("page=")[-1]

                yield Request(response.url+'&page={j}'.format(
                                                       j=int(page) + 1),
                    self.parse_homepage_for_followers_and_fans, dont_filter=True)
            else:
                yield Request(response.url+'&page={j}'.format(
                                                       j=2),
                    self.parse_homepage_for_followers_and_fans, dont_filter=True)
