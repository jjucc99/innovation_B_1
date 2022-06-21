from flask import *
import requests
from pymongo import MongoClient

#pymongo
client = MongoClient('mongodb+srv://test:sparta@cluster0.yqzgz.mongodb.net/?retryWrites=true&w=majority')
db = client.dbsparta

#flask
app = Flask(__name__)


@app.route('/')
def main():
    return render_template("index.html")


@app.route('/diet')
def detail():
    return render_template("sub.html")


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)