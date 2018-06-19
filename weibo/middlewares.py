# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
import logging
import requests
import json
import random
import redis
from scrapy.exceptions import IgnoreRequest
from weibo import settings
import base64

class WeiboSpiderMiddleware(object):
    def __init__(self):
        self.logger=logging.getLogger(__name__)


    def get_cookies(self):
        r=redis.Redis(host='localhost',port=6379)
        f=r.keys()
        cookies=[]
        for i in f:
            if 'weibo' in str(i):
                  cookies.append(r.get(i))
        p=random.randint(0,len(cookies)-1)
        return (cookies[p])

    def process_requests(self):
        requests.cookie=self.get_cookies()
        if requests.status ==  '403':
            logging.info('cookie is invaild')
            requests.cookie=self.get_cookies1()
        else:
            logging.info('cookie is vaild')
class ProxyMiddleware(object):

    def process_request(self, request, spider):
        proxy_server = 'http://http-dyn.abuyun.com:9020'
        proxy_user = 'HY14U6L8TSLR0IHD'
        proxy_pass = '42538E56B98F3D63'

        proxy_auth = "Basic " + base64.urlsafe_b64encode(bytes((proxy_user + ":" + proxy_pass), "ascii")).decode("utf8")
        request.meta["proxy"] = proxy_server
        request.headers["Proxy-Authorization"] = proxy_auth

# class WeiboSpiderMiddleware(object):
#       def __init__(self,cookies_pool_url):
#           self.logger=logging.getLogger(__name__)
#           self.cookies_pool_url=cookies_pool_url
#
#       def get_random_cookies(self):
#           try:
#               response=requests.get(self.cookies_pool_url)
#               if response.status_code == 200:
#                   return json.loads(response.text)
#           except ConnectionError:
#               return None
#
#       def process_request(self,request,spider):
#           cookies=self.get_random_cookies()
#           if cookies:
#               requests.cookies=cookies
#               self.logger.debug('using cookies'+json.dumps(cookies))
#           else:
#               self.logger.debug('no vaild cookies')
#
#       @classmethod
#       def from_crawler(cls,crawler):
#           return cls(
#               cookies_pool_url=crawler.setting.get('COOKIES_POOL_URL')
#           )
#
#       def process_response(self,request,response,spider):
#           if response.status in [300,301,302,303]:
#               try:
#                   redirect_url=response.headers['location']
#                   if 'login.weibo' in redirect_url or 'login.sina' in redirect_url:
#                       self.logger.warning('updataing cookies')
#                   elif 'weibo.cn/security' in redirect_url:
#                       self.logger.warning('now cookies'+json.dumps(request.cookies))
#                       self.logger.warning('one account is locked')
#                   request.cookies=self.get_random_cookies()
#                   self.logger.debug('using cookies'+json.dumps(request.cookies))
#                   return request
#               except Exception:
#                   raise IgnoreRequest
#           elif response.status in [414]:
#               return request
#           else:
#               return  response
