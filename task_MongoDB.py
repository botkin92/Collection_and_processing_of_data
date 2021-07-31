from pprint import pprint
import json
from pymongo import MongoClient


def writing_to_db(json_file, mongo_client, mongo_db="test", mongo_coll="dataset"):
    db = mongo_client[mongo_db]
    coll = db[mongo_coll]
    with open('parse_hh.json', encoding='utf8') as f:
        json_data = json.load(f)
    for elem in json_data:
        coll.update_one({"link": {'$eq': elem["link"]}}, {'$set': elem}, upsert=True)
    mongo_client.close()


def find_salary_in_db(mongo_client, mongo_db="test", mongo_coll="dataset", amount=0):
    db = mongo_client[mongo_db]
    coll = db[mongo_coll]
    for vacancy in coll.find({"salary_min": {'$gt': amount}}):
        pprint(vacancy)


MONGO_HOST = 'localhost'
MONGO_PORT = 27017
MONGO_DB = 'vacancy'
MONGO_COLLECTION = 'vacancy_hh'

my_client = MongoClient(MONGO_HOST, MONGO_PORT)
writing_to_db('parse_hh.json', my_client, MONGO_DB, MONGO_COLLECTION)

input_salary = int(input('Введите минимальную зарплату: '))
find_salary_in_db(my_client, MONGO_DB, MONGO_COLLECTION, input_salary)
