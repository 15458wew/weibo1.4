# -*- encoding: utf-8 -*-

import logging
from weibo.BloomFilterRedis import BloomFilterRedis
from scrapy.dupefilters import BaseDupeFilter


class BloomRedisDupeFilter(BaseDupeFilter):

    hash_list = ["rs_hash", "js_hash", "pjw_hash", "elf_hash", "bkdr_hash",
                 "sdbm_hash", "djb_hash", "dek_hash"]

    def __init__(self, key="bloom", host="localhost", port=6379,password='Passw0rd',
                 hash_list=hash_list, debug=False):
        self.bloomFilterRedis = BloomFilterRedis(
            key=key, host=host, port=port,hash_list=hash_list)
        self.logdupes = True
        self.debug = debug
        self.logger = logging.getLogger(__name__)

    @classmethod
    def from_settings(cls, settings):
        key = settings['BLOOM_REDIS_KEY']
        if key is None:
            key = "bloom"
        host = settings['BLOOM_REDIS_HOST']
        if host is None:
            #host = "r-2zec10d55c9ead54.redis.rds.aliyuncs.com"
            host='localhost'
        port = settings['BLOOM_REDIS_PORT']
        if port is None:
            port = 6379
        # password=settings['BLOOM_REDIS_PASSWORD']
        # if password is None:
        #     password='Passw0rd'
        hash_list = settings['BLOOM_REDIS_HASH_LIST']
        if hash_list is None:
            hash_list = BloomRedisDupeFilter.hash_list
        debug = settings.getbool('DUPEFILTER_DEBUG')
        return cls(key, host, port, hash_list, debug)

    def request_seen(self, request):
        re = self.bloomFilterRedis.do_filter(request.url)
        # with open("allurl.txt", "a") as f:
        #     f.write(request.url+'\n')
        if re is False:
            # with open("filted.txt", "a") as f:
            #     f.write(request.url+'\n')
            return True

    def close(self, reason):
        self.bloomFilterRedis.pool.disconnect()

    def log(self, request, spider):
        if self.debug:
            msg = "Filtered duplicate request: %(request)s"
            self.logger.debug(msg, {'request': request}, extra={'spider': spider})
        elif self.logdupes:
            msg = ("Filtered duplicate request: %(request)s"
                   " - no more duplicates will be shown"
                   " (see DUPEFILTER_DEBUG to show all duplicates)")
            self.logger.debug(msg, {'request': request}, extra={'spider': spider})
            self.logdupes = False

        spider.crawler.stats.inc_value('dupefilter/filtered', spider=spider)
