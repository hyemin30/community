from flask import Flask, render_template, jsonify, request, make_response
from pymongo import MongoClient

client = MongoClient('mongodb+srv://test:sparta@cluster0.jftxkcu.mongodb.net/?retryWrites=true&w=majority')
db = client.community
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

#프로필 목록
@app.route('/profile', methods=["GET"])
def profile():
    profile_list = list(db.users.find({}, {'_id': False}))
    return jsonify({'profile': profile_list})

#게시글 목록
@app.route('/postings', methods=["GET"])
def profile():
    posting_list = list(db.postings.find({}, {'_id': False}))
    return jsonify({'postings': posting_list})

#읽음
@app.route('/read', methods=["POST"])
def profile():
    num_receive = request.form['num_give']
    db.postings.update_one({'num': int(num_receive)}, {'$set': {'read': 1}})
    return jsonify({'msg': '읽기 완료'})

#게시글 작성
@app.route('/posting', methods=["POST"])
def profile():
    postings = list(db.postings.find({}, {'_id': False}))
    content_receive = request.form['content_give']

    doc = {
        'num' : len(postings)+1,
        'read' : 0,
        'content' : content_receive
    }
    db.content.insert_one(doc)
    return jsonify({'msg': '작성 완료'})













