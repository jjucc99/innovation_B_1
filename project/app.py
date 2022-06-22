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
    week = []

    i = 0
    while i <= 6:
        users = list(db.prac.find({'day': str(i)}, {'_id': False}))
        if len(users) != 0:
            week.append(users)
        i = i + 1

    diet = []
    total = 0

    list_menu = None
    j = 0

    for day in week:
        while j < len(day):
            if int(day[j]['mainkcal']) + int(day[j]['subkcal']) > total:
                total = int(day[j]['mainkcal']) + int(day[j]['subkcal'])
                list_menu = day[j]
            j = j + 1
        j = 0
        total = 0
        if list is not None:
            diet.append(list_menu)
        list_menu = None

    return render_template("index.html", diet=diet, year=year, month=month)

@app.route('/diet/<day>')
def detail(day):
    # print(day)
    year = datetime.today().year
    month = datetime.today().month
    users = list(db.prac.find({'day': str(day)}, {'_id': False}))
    return render_template("sub.html", month=month, year=year, user=users)

@app.route('/')
def home():
    return render_template("index.html")

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

@app.route("/sub/comment", methods=["POST"])
def sub_post():
    time_receive = request.form['times_give']
    day_receive = request.form['date_give']
    comment_receive = request.form['comment_give']

    doc = {
        'time' : time_receive,
        'day' : day_receive,
        'comment' : comment_receive
    }

    db.subcomment.insert_one(doc)
    return jsonify({'msg':'저장 완료!'})

@app.route("/sub/comment/<day>/<time>", methods=["GET"])
def get_comment(day,time):
    users = list(db.subcomment.find({'day':day,'time':time}, {'_id': False}))
    # print(day+time)
    return jsonify({'users':users})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)