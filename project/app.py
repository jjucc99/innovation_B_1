from flask import *
import requests
from datetime import datetime
from pymongo import MongoClient

#pymongo
# client = MongoClient('mongodb+srv://test:sparta@cluster0.yqzgz.mongodb.net/?retryWrites=true&w=majority')
# db = client.dbsparta
client = MongoClient('mongodb+srv://test:sparta@cluster0.fchsu.mongodb.net/Cluster0?retryWrites=true&w=majority')
db = client.dbsparta

#flask
app = Flask(__name__)

@app.route('/')
def main():
    year = datetime.today().year
    month = datetime.today().month
    days = [[{"day": 0,
              "time": 1,
              "main": "우동",
              "mainkcal": 2000,
              "sub": "김치",
              "subkcal": 500,
              "img": "https://file.mk.co.kr/meet/neds/2017/09/image_readtop_2017_587233_15042337473013492.jpg"},
             {"day": 0,
              "tme": 0,
              "main": "라면",
              "mainkcal": 1500,
              "sub": "김치",
              "subkcal": 500,
              "img": "https://file.mk.co.kr/meet/neds/2017/09/image_readtop_2017_587233_15042337473013492.jpg"},
             {"day": 0,
              "tme": 2,
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
              "img": "https://file.mk.co.kr/meet/neds/2017/09/image_readtop_2017_587233_15042337473013492.jpg"},
             {"day": 1,
              "time": 2,
              "main": "짜장면",
              "mainkcal": 900,
              "sub": "김치",
              "subkcal": 500,
              "img": "https://file.mk.co.kr/meet/neds/2017/09/image_readtop_2017_587233_15042337473013492.jpg"}
             ]
            ]
    diet = []
    total = 0
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
    print(day)
    return render_template("sub.html")

@app.route('/diet/input')
def input_page():
    return render_template("sub_input_form.html")

@app.route('/diet/input_menu', methods=["POST"])

def input_menu():
    day_receive = request.form['day_give']
    time_receive = request.form['time_give']
    main_receive = request.form['main_give']
    mainkcal_receive = request.form['mainkcal_give']
    img_receive = request.form['img_give']
    sub_receive = request.form['sub_give']
    subkcal_receive = request.form['subkcal_give']

    doc = {
        'day' : day_receive,
        'time' : time_receive,
        'main' : main_receive,
        'mainkcal' : mainkcal_receive,
        'img' : img_receive,
        'sub' : sub_receive,
        'subkcal' : subkcal_receive
    }

    users = list(db.prac.find({'day': day_receive}, {'_id': False}))

    for user in users :
        if user['time'] == doc['time']:
            return jsonify({'msg': '작성한 이력이 있습니다.'})
        else :
            db.prac.insert_one(doc)
            return jsonify({'msg': '입력완료'})

    db.prac.insert_one(doc)
    return jsonify({'msg': '입력완료'})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)