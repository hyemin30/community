<<<<<<< Updated upstream
=======
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
    email = request.cookies.get("emailCookie")
    posting_list = list(db.postings.find({}, {'_id': False}))
    reading_list = list(db.read.find({'email': email}, {'_id': False}))
    return jsonify({'postings': posting_list, 'readings': reading_list})

#읽음
@app.route('/read', methods=["POST"])
def read():
    num_receive = request.form['num_give']
    email = request.cookies.get("emailCookie")

    doc = {
        'num': num_receive,
        'email': email
    }
    db.read.insert_one(doc)

    return jsonify({'msg': '읽기 완료'})

#게시글 작성
@app.route('/posting', methods=["POST"])
def posting():
    email = request.cookies.get("emailCookie")
    postings = list(db.postings.find({}, {'_id': False}))
    content_receive = request.form['content_give']

    doc = {
        'num' : len(postings)+1,
        'content' : content_receive,
        'email':email
    }
    db.content.insert_one(doc)
    return jsonify({'msg': '작성 완료'})

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
    content_receive = request.form['post_give']
    db.postings.update_one({'num': num_receive}, {'$set': {'content': content_receive}})
    return jsonify({'msg': '작성 완료'})


#좋아요
@app.route('/like', methods=["POST"])
def like():
    num_receive = request.form['num_give']
    email = request.cookies.get("emailCookie")
    likes = list(db.likes.find({"num", num_receive}, {'_id': False}))
    count = len(likes)

    for like in likes:
        if email == like['email']:
            return jsonify({'msg': '이미 좋아요를 눌렀습니다'})

    doc = {
        'num': num_receive,
        'email': email,
        'count': count + 1
    }
    db.likes.insert_one(doc)
    return jsonify({'msg': '좋아요 완료'})

#회원가입 페이지
@app.route("/join", methods=["GET"])
def join_get():
    return '회원가입 페이지'


#회원 가입
@app.route("/join", methods=["POST"])
def join_post():
    email_receive = request.form['email_give']
    passwd_receive = request.form['passwd_give']
    name_receive = request.form['name_give']
    lang_receive = request.form['lang_give']
    blog_url_receive = request.form['blog_url_give']

    member_list = list(db.members.find({}, {'_id': False}))

    for member in member_list:
        if member['email'] == email_receive:
            return "이미 가입된 이메일 주소입니다."


    if email_receive == "" or passwd_receive == "" or name_receive == "" or lang_receive == "":
        return "필수값을 입력해주세요."

    doc = {
        'email': email_receive,
        'passwd': passwd_receive,
        'name': name_receive,
        'lang': lang_receive,
        'blog_url': blog_url_receive
    }
    db.members.insert_one(doc)

    return jsonify({'msg': '가입 완료'})


#로그인 페이지
@app.route("/login", methods=["GET"])
def login_get():
    return "로그인 페이지"

#로그인
@app.route("/login", methods=['POST'])
def login_post():
    email_receive = request.form['email_give']
    passwd_receive = request.form['passwd_give']

    login_member = db.members.find_one({"email": email_receive})

    if login_member['passwd'] == passwd_receive:
        response = make_response()
        response.set_cookie('emailCookie', login_member['email'])

        return response
    else:
        return '비밀번호가 일치하지 않습니다.'


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)









>>>>>>> Stashed changes
