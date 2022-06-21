from flask import *
import requests
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
    return render_template("index.html")

@app.route('/diet')
def detail():
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