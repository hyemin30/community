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
def postings():
    posting_list = list(db.postings.find({}, {'_id': False}))
    return jsonify({'postings': posting_list})

#게시글 수정화면
@app.route('/edit', methods=["GET"])
def edit_form():
    num_receive = request.form['num_give']
    posting = db.postings.find_one({'num': num_receive})
    return jsonify({'posting': posting})

#게시글 수정등록
@app.route('/edit', methods=["POST"])
def edit():
    num_receive = request.form['num_give']
    content_receive = request.form['content_give']
    db.postings.update_one({'num': num_receive}, {'$set': {'content': content_receive}})
    return jsonify({'msg': '작성 완료'})

#읽음
@app.route('/read', methods=["POST"])
def read():
    num_receive = request.form['num_give']
    db.postings.update_one({'num': int(num_receive)}, {'$set': {'read': 1}})
    return jsonify({'msg': '읽기 완료'})

#게시글 작성
@app.route('/posting', methods=["POST"])
def posting():
    postings = list(db.postings.find({}, {'_id': False}))
    content_receive = request.form['content_give']
    email = request.cookies.get("email")

    doc = {
        'num' : len(postings)+1,
        'read' : 0,
        'content' : content_receive,
        'email': email
    }
    db.content.insert_one(doc)
    return jsonify({'msg': '작성 완료'})

#좋아요
@app.route('/like', methods=["POST"])
def like():
    num_receive = request.form['num_give']
    content_receive = request.form['content_give']
    db.postings.update_one({'num': num_receive}, {'$set': {'content': content_receive}})
    return jsonify({'msg': '작성 완료'})











