import jwt
import datetime
import hashlib
import requests
from flask import Flask, render_template, jsonify, request, redirect, url_for
from datetime import datetime, timedelta
from werkzeug.utils import secure_filename




app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config['UPLOAD_FOLDER'] = "./static/profile_pics"

SECRET_KEY = 'SPARTA'
from pymongo import MongoClient
client = MongoClient("mongodb+srv://test:sparta@cluster0.qtj5c.mongodb.net/Cluster0?retryWrites=true&w=majority")
db = client.dbsparta


@app.route('/')
def home():

    token_receive = request.cookies.get('mytoken')
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

    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])

        return render_template("index.html", diet=diet, year=year, month=month)
    except jwt.ExpiredSignatureError:
        return redirect(url_for("login", msg="로그인 시간이 만료되었습니다."))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("login", msg="로그인 정보가 존재하지 않습니다."))


@app.route('/login')
def login():
    msg = request.args.get("msg")
    return render_template('login.html', msg=msg)


@app.route('/sign_in', methods=['POST'])
def sign_in():
    username_receive = request.form['username_give']
    password_receive = request.form['password_give']

    pw_hash = hashlib.sha256(password_receive.encode('utf-8')).hexdigest()
    result = db.users.find_one({'username': username_receive, 'password': pw_hash})

    if result is not None:
        payload = {
         'id': username_receive,
         'exp': datetime.utcnow() + timedelta(seconds=60 * 60 * 24)
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256').decode('utf-8')

        return jsonify({'result': 'success', 'token': token})
    else:
        return jsonify({'result': 'fail', 'msg': '아이디/비밀번호가 일치하지 않습니다.'})


@app.route('/sign_up/save', methods=['POST'])
def sign_up():
    username_receive = request.form['username_give']
    password_receive = request.form['password_give']
    password_hash = hashlib.sha256(password_receive.encode('utf-8')).hexdigest()
    doc = {
        "username": username_receive,                               # 아이디
        "password": password_hash,                                  # 비밀번호
        # "profile_name": username_receive,                           # 프로필 이름 기본값은 아이디
    }
    db.users.insert_one(doc)
    return jsonify({'result': 'success'})


@app.route('/sign_up/check_dup', methods=['POST'])
def check_dup():
    username_receive = request.form['username_give']
    exists = bool(db.users.find_one({"username": username_receive}))
    return jsonify({'result': 'success', 'exists': exists})

@app.route('/diet/<day>')
def detail(day):
    # print(day)
    year = datetime.today().year
    month = datetime.today().month
    users = list(db.prac.find({'day': str(day)}, {'_id': False}))
    return render_template("sub.html", month=month, year=year, user=users)

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