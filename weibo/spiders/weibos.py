# -*- coding: utf-8 -*-
from scrapy import Spider,Request,FormRequest
import scrapy
from scrapy.selector import Selector
import json

import logging as log
from weibo.items import InformationItem,TweetsItem


class WeibosSpider(scrapy.Spider):
    name = 'weibos'
    allowed_domains = ['m.weibo.cn']
    start_url = 'https://m.weibo.cn/api/container/getSecond?containerid={include}'
    start_include='1005053905389155_-_FOLLOWERS'
    follow_url='https://m.weibo.cn/api/container/getIndex?containerid=231051_-_followers_-_{weiboid}&featurecode=2000320'
    follow_url_next='https://m.weibo.cn/api/container/getIndex?containerid=231051_-_followers_-_{weiboid}&featurecode=20000320&page={j}'

    follow_profile_url='https://m.weibo.cn/api/container/getIndex?uid={weiboid}&luicode=10000012&lfid={lfid}&type=uid&value={weiboid}&containerid=107603{weiboid}'
    follow_profile_url_1='https://m.weibo.cn/api/container/getIndex?uid={weiboid}&luicode=10000012&lfid=231051_-_follow_-_{last_id}&type=uid&value={weiboid}&containerid=107603{weiboid}'
    follow_profile_url_next='https://m.weibo.cn/api/container/getIndex?uid={weiboid}&luicode=10000012&lfid={lfid}&type=uid&value={weiboid}&containerid=107603{weiboid}&page={j}'
    follow_profile_url_1_next = 'https://m.weibo.cn/api/container/getIndex?uid={weiboid}&luicode=10000012&lfid=231051_-_follow_-_{last_id}&type=uid&value={weiboid}&containerid=107603{weiboid}&page={j}'

    start_followers_url='https://m.weibo.cn/api/container/getSecond?containerid=1005053905389155_-_FANS'
    followers_url='https://m.weibo.cn/api/container/getIndex?containerid=231051_-_fans_-_{weiboid}&featurecode=20000320'
    followers_url_next='https://m.weibo.cn/api/container/getIndex?containerid=231051_-_fans_-_{weiboid}&featurecode=20000320&since_id={j}'
    followers_profile_url='https://m.weibo.cn/api/container/getIndex?uid={weiboid}&luicode=10000011&lfid=231051_-_fans_-_{last_id}&featurecode=20000320&type=uid&value={weiboid}&containerid=107603{weiboid}'

    def start_requests(self):
        yield Request(self.start_url.format(include=self.start_include),self.parse_user)

    def parse_user(self, response):
        json_object = json.loads(response.body_as_unicode())
        weiboItem = InformationItem()
        count=-1
        for i in json_object['data']['cards']:
            count+=1
        for i in range(count):
            weiboItem['screen_name'] = json_object['data']['cards'][i]['user']['screen_name']
            weiboItem['description'] = json_object['data']['cards'][i]['user']['description']
            weiboItem['follow_count'] = json_object['data']['cards'][i]['user']['follow_count']
            weiboItem['followers_count'] = json_object['data']['cards'][i]['user']['followers_count']
            weiboItem['gender'] = json_object['data']['cards'][i]['user']['gender']
            weiboItem['id'] = json_object['data']['cards'][i]['user']['id']
            weiboItem['profile_url'] = json_object['data']['cards'][i]['user']['profile_url']
            if json_object['data']['cards'][i]['user']['verified']==True:
                weiboItem['verified_reason'] = json_object['data']['cards'][i]['user']['verified_reason']
            else:
                weiboItem['verified_reason']=None
            yield weiboItem
            yield Request(self.follow_profile_url.format(weiboid=weiboItem['id'],lfid=self.start_include),self.parse_homepage,dont_filter=False)
            yield Request(self.follow_url.format(weiboid=weiboItem['id']), self.parse_follows,dont_filter=False)
            yield Request(self.followers_url.format(weiboid=weiboItem['id']),self.parse_followers)
            #for i in range(1,20):
                #yield Request(self.follow_profile_url_next.format(profile_url=weiboItem['profile_url'],i=i),self.parse_homepage)

    def parse_follows(self,response):
        json_object_follows=json.loads(response.body_as_unicode())
        last_id=json_object_follows['data']['cardlistInfo']['containerid'][6:]
        weiboItem=InformationItem()
        try:
            count = -1
            for i in json_object_follows['data']['cards']:
                count += 1
            for i in range(9):
                weiboItem['screen_name'] = json_object_follows['data']['cards'][count]['card_group'][i]['user']['screen_name']
                weiboItem['description'] = json_object_follows['data']['cards'][count]['card_group'][i]['user']['description']
                weiboItem['follow_count'] = json_object_follows['data']['cards'][count]['card_group'][i]['user']['follow_count']
                weiboItem['followers_count'] = json_object_follows['data']['cards'][count]['card_group'][i]['user']['followers_count']
                weiboItem['gender'] = json_object_follows['data']['cards'][count]['card_group'][i]['user']['gender']
                weiboItem['id'] = json_object_follows['data']['cards'][count]['card_group'][i]['user']['id']
                weiboItem['profile_url'] = json_object_follows['data']['cards'][count]['card_group'][i]['user']['profile_url']
                if json_object_follows['data']['cards'][count]['card_group'][i]['user']['verified'] == True:
                    weiboItem['verified_reason'] = json_object_follows['data']['cards'][count]['card_group'][i]['user']['verified_reason']
                else:
                    weiboItem['verified_reason'] = None
                yield weiboItem
                yield Request(self.follow_profile_url_1.format(weiboid=weiboItem['id'],last_id=last_id),
                              self.parse_homepage, dont_filter=False)
                yield Request(self.follow_url.format(weiboid=weiboItem['id']), self.parse_follows,dont_filter=False)
                yield Request(self.followers_url.format(weiboid=weiboItem['id']),self.parse_followers,dont_filter=False)
                for j in range(10):
                    count=j
                    yield Request(self.follow_url_next.format(weiboid=weiboItem['id'],j=count),self.parse_homepage)

        except Exception as e:
            pass
                #for i in range(9):
                    #yield Request(self.follow_profile_url_next.format())

    def parse_followers(self,response):
        json_object = json.loads(response.body_as_unicode())
        last_id=json_object['data']['cardlistInfo']['containerid'][6:]
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
            if json_object['data']['cards'][i]['user']['verified'] == True:
                weiboItem['verified_reason'] = json_object['data']['cards'][i]['user']['verified_reason']
            else:
                weiboItem['verified_reason'] = None
            yield weiboItem
            yield Request(self.followers_profile_url.format(weiboid=weiboItem['id'],last_id=last_id),self.parse_homepage)
            for j in range(10):
                count=j
                yield Request(self.followers_url_next.format(weiboid=weiboItem['id'],j=count),self.parse_followers)

    def parse_homepage(self,response):
        json_homepage=json.loads(response.body_as_unicode())
        tweetsitem=TweetsItem()
        try:
           tweetsitem['id']=json_homepage['data']['cardlistInfo']['containerid'][6:]
           for i in range(10):
                if json_homepage['data']['cards'][i]['card_type'] ==9:
                    tweetsitem['screen_name']=json_homepage['data']['cards'][i]['mblog']['user']['screen_name']
                    tweetsitem['text']=json_homepage['data']['cards'][i]['mblog']['text']
                    tweetsitem['created_at']=json_homepage['data']['cards'][i]['mblog']['created_at']
                    tweetsitem['attitudes_count']=json_homepage['data']['cards'][i]['mblog']['attitudes_count']
           yield tweetsitem
           for i in range(1,10):
               count=i
               yield Request(self.follow_profile_url_1_next.format(weiboid=tweetsitem['id'],j=count),self.parse_homepage_next)
        except Exception as e:
               pass

    def parse_homepage_next(self,response):
        json_homepage = json.loads(response.body_as_unicode())
        tweetsitem = TweetsItem()
        try:
            tweetsitem['id'] = json_homepage['data']['cardlistInfo']['containerid'][6:]
            for i in range(10):
                  if json_homepage['data']['cards'][i]['card_type'] == 9:
                       tweetsitem['screen_name'] = json_homepage['data']['cards'][i]['mblog']['user']['screen_name']
                       tweetsitem['text'] = json_homepage['data']['cards'][i]['mblog']['text']
                       tweetsitem['created_at'] = json_homepage['data']['cards'][i]['mblog']['created_at']
                       tweetsitem['id_top']=json_homepage['data']['cards'][i]['mblog']['is_top']
                       tweetsitem['attitudes_count'] = json_homepage['data']['cards'][i]['mblog']['attitudes_count']
            yield tweetsitem
        except Exception as e:
            pass
