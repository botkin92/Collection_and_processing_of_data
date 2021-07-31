from lxml import html
from pprint import pprint
import requests
from pymongo import MongoClient

header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Safari/537.36'}


def news_mailru():
    global header
    all_news = []
    response1 = requests.get('https://news.mail.ru/', headers=header)
    dom1 = html.fromstring(response1.text)
    link_list = dom1.xpath("//div[contains(@class, 'daynews__item')]/a/@href")
    for url in link_list:
        response2 = requests.get(url, headers=header)
        dom2 = html.fromstring(response2.text)
        news = {}
        news['name'] = dom2.xpath("//h1/text()")[0]
        news['link'] = url
        news['date'] = dom2.xpath("//span[@datetime]/@datetime")[0]
        news['source'] = dom2.xpath("//a[contains(@class, 'breadcrumbs__link')]/@href")[0]
        all_news.append(news)
    return all_news


def news_lentaru():
    global header
    all_news = []
    url = 'https://lenta.ru'
    response = requests.get(url, headers=header)
    dom = html.fromstring(response.text)
    items = dom.xpath("////time[contains(@class, 'g-time')]")
    for item in items:
        news = {}
        news['name'] = item.xpath("./../text()")[0].replace('\xa0', ' ')
        news['link'] = url + item.xpath("./../@href")[0]
        news['date'] = item.xpath("./@datetime")[0]
        news['source'] = 'https://lenta.ru'
        all_news.append(news)
    return all_news


def writing_to_db(json_data, mongo_db="test", mongo_coll="dataset"):
    global MONGO_HOST, MONGO_PORT
    mongo_client = MongoClient(MONGO_HOST, MONGO_PORT)
    db = mongo_client[mongo_db]
    coll = db[mongo_coll]
    for elem in json_data:
        coll.update_one({"link": {'$eq': elem["link"]}}, {'$set': elem}, upsert=True)
    mongo_client.close()


news_resp1 = news_mailru()
news_resp2 = news_lentaru()
# pprint(news_resp1)
# pprint(news_resp2)

MONGO_HOST = 'localhost'
MONGO_PORT = 27017

writing_to_db(news_resp1, 'news', 'main_news')
writing_to_db(news_resp2, 'news', 'main_news')
