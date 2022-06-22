# from flask import *
import requests
from datetime import datetime
from pymongo import MongoClient

#pymongo
# client = MongoClient('mongodb+srv://test:sparta@cluster0.yqzgz.mongodb.net/?retryWrites=true&w=majority')
# db = client.dbsparta
client = MongoClient('mongodb+srv://test:sparta@cluster0.fchsu.mongodb.net/Cluster0?retryWrites=true&w=majority')
db = client.dbsparta

#flask
# app = Flask(__name__)


week = []

i = 0
while i <= 6:
    users = list(db.prac.find({'day': str(i)}, {'_id': False}))
    if len(users) != 0:
        week.append(users)
    i = i + 1

diet = []
total = 0

users = list(db.prac.find({'day': '0'}, {'_id': False}))
print(users)
# list = None
# j = 0


# for day in week:
#     while j < len(day):
#         if int(day[j]['mainkcal']) + int(day[j]['subkcal']) > total:
#             total = int(day[j]['mainkcal']) + int(day[j]['subkcal'])
#             list = day[j]
#         j = j+1
#     j = 0
#     total = 0
#     if list is not None:
#         diet.append(list)
#     list = None
# 
