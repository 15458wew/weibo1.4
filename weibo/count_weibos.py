#based on mongodb and elasticsearch for count
import pymongo
import elasticsearch
from pymongo import MongoClient
import datetime,time
from elasticsearch import Elasticsearch
#from .settings import MONGO_PORT,MONGO_URL,ELASTICSEARCH_URL,MONGO_DB,START_TIME

def get_counts():
    client=MongoClient(host=MONGO_URL,port=MONGO_PORT,db=MONGO_DB)
    db=client.weibo
    weibo_tweets=db.weibo_tweets
    weibo_users_information=db.weibo_users_information
    print('the numbers of weibo_tweets is',weibo_tweets.count())
    print('the numbers of weibo_users_information is',weibo_users_information.count())
    elk_for_vision(weibo_tweets.count(),weibo_users_information.count())
def timer():
    sched_time=datetime.datetime(START_TIME)
    timedelta=datetime.timedelta(minutes=1)
    now=datetime.datetime.now()
    if str(sched_time-now)[0]=='-':
        print('开始时间已经错过，请调整时间')
    else:
        while True:
            now=str(datetime.datetime.now())[:-7]
            if now==str(sched_time):
                print(sched_time)
                sched_time=str(datetime.datetime.now()+timedelta)[:-7]
                get_counts()
            time.sleep(1)
def elk_for_vision(m,n):
    es=Elasticsearch(ELASTICSEARCH_URL)
    data={
        "@timestamp":datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.000+0800"),
        "weibo":"404",
        "weibo_tweets_count":m,
        "weibo_user_information_count":n
    }
    es.index(index='weibo',doc_type='count',body=data)
if __name__ == '__main__':
    timer()
