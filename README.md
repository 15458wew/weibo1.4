
# weibo1.4

scrapy_redis抓取新浪微博下所有大v，蓝v的个人信息以及所发微博
elasticsearch_monitor监控所抓信息并存入到elasticsearch模块，利用kibana进行展示
bluefilter模块将布隆过滤器替换掉redis的请求队列，极大的缩短了所用时间与空间。

 1.bluefilter文件包括：BloomFilterRedis.py BloomRedisDupeFilter.py GeneralHashFunctions.py. 将三者放入settings.py同目录下即可 
 2.settings.py中将 DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter" 改为 DUPEFILTER_CLASS = "weibo.BloomRedisDupeFilter.BloomRedisDupeFilter
