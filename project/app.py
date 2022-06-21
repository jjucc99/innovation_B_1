from flask import *
from datetime import datetime

import requests
from pymongo import MongoClient

# pymongo
client = MongoClient('mongodb+srv://test:sparta@cluster0.yqzgz.mongodb.net/?retryWrites=true&w=majority')
db = client.dbsparta

# flask
app = Flask(__name__)


@app.route('/')
def main():
    year = datetime.today().year
    month = datetime.today().month

    days = [[{"day": 0,
              "time": 0,
              "main": "라면",
              "mainkcal": 1500,
              "sub": "김치",
              "subkcal": 500,
              "img": "https://file.mk.co.kr/meet/neds/2017/09/image_readtop_2017_587233_15042337473013492.jpg"},
             {"day": 0,
              "time": 1,
              "main": "우동",
              "mainkcal": 2000,
              "sub": "김치",
              "subkcal": 500,
              "img": "https://file.mk.co.kr/meet/neds/2017/09/image_readtop_2017_587233_15042337473013492.jpg"},
             {"day": 0,
              "time": 2,
              "main": "짜장면",
              "mainkcal": 900,
              "sub": "김치",
              "subkcal": 500,
              "img": "https://file.mk.co.kr/meet/neds/2017/09/image_readtop_2017_587233_15042337473013492.jpg"}
             ],
            [{"day": 1,
              "time": 0,
              "main": "라면",
              "mainkcal": 1500,
              "sub": "김치",
              "subkcal": 500,
              "img": "https://file.mk.co.kr/meet/neds/2017/09/image_readtop_2017_587233_15042337473013492.jpg"},
             {"day": 1,
              "time": 1,
              "main": "우동",
              "mainkcal": 2000,
              "sub": "김치",
              "subkcal": 500,
              "img": "https://media.istockphoto.com/photos/japanese-food-udon-noodle-soup-picture-id1150113717?k=20&m=1150113717&s=612x612&w=0&h=FZzMW6RCFTSt8_lnamYLgwzgYJ_fmYqHsCkB8ePSV40="},
             {"day": 1,
              "time": 2,
              "main": "짜장면",
              "mainkcal": 6000,
              "sub": "김치",
              "subkcal": 500,
              "img": "https://recipe1.ezmember.co.kr/cache/recipe/2021/10/26/8f82be9c22ec2f4f9ab25363cc611b141.jpg"}
             ],
            ]
    diet = []
    total = 0
    one = None

    for day in days:
        for someday in day:
            someday_kcal = someday['mainkcal'] + someday['subkcal']
            if someday_kcal > total:
                total = someday_kcal
                one = someday
        total = 0
        diet.append(one)

    return render_template("index.html", diet=diet, year=year, month=month)


@app.route('/diet/<day>')
def detail(day):

    return render_template("sub.html", day=day)


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
