from importlib.resources import contents

from flask import Flask, render_template, jsonify, request, make_response
from pymongo import MongoClient

# client = MongoClient('mongodb+srv://test:sparta@cluster0.jftxkcu.mongodb.net/?retryWrites=true&w=majority')
# db = client.community

client = MongoClient('mongodb+srv://test:Dmg0ltfaNgmxokj5@cluster0.jhc3fyv.mongodb.net/Cluster0?retryWrites=true&w=majority')
db = client.dbsparta
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

#프로필 목록
@app.route('/profile', methods=["GET"])
def profile():
    profile_list = list(db.members.find({}, {'_id': False}))
    return jsonify({'profile': profile_list})

#게시글 목록
@app.route('/post', methods=["GET"])
def postings():
    email = request.cookies.get("emailCookie")
    readings = list(db.read.find({'email': email}, {'_id': False}))
    return jsonify({'readings': readings})

#읽음
@app.route('/read', methods=["POST"])
def read():
    num_receive = int(request.form['num_give'])
    email = request.cookies.get("emailCookie")

    db.read.update_one({'email': email, 'num':num_receive}, {'$set': {'read': 1}})
    return jsonify({'msg': '읽기 완료'})

#게시글 작성
@app.route('/post', methods=["POST"])
def posting():
    postings = list(db.postings.find({}, {'_id': False}))
    content_receive = request.form['content_give']

    if content_receive == '' or content_receive is None:
        return jsonify({'msg': '내용을 작성해주세요'})

    doc = {
        'num': len(postings)+1,
        'content': content_receive,
    }
    db.postings.insert_one(doc)

    members = list(db.members.find({}, {'_id': False}))

    for member in members:
        doc = {
            'num': len(postings) + 1,
            'content': content_receive,
            'email': member['email'],
            'read': 0
        }
        db.read.insert_one(doc)
    return jsonify({'msg': '작성 완료'})
#########################임시###############################
# #게시글 수정화면
# @app.route('/edit', methods=["GET"])
# def edit_form():
#     num_receive = request.form['num_give']
#     posting = db.postings.find_one({'num': num_receive})
#     return jsonify({'posting': posting})
#
# #게시글 수정등록
# @app.route('/edit', methods=["POST"])
# def edit():
#     num_receive = request.form['num_give']
#     content_receive = request.form['post_give']
#
#     if content_receive == '' or content_receive is None:
#         return jsonify({'msg': '내용을 작성해주세요'})
#
#     db.postings.update_one({'num': num_receive}, {'$set': {'content': content_receive}})
#     return jsonify({'msg': '작성 완료'})
#
#
# #좋아요
# @app.route('/like', methods=["POST"])
# def like():
#     # num_receive = int(request.form['num_give'])
#     # email = request.cookies.get("emailCookie")
#     num_receive = 3
#     email='test2@naver.com'
#     likes = list(db.likes.find({'num', num_receive}, {'_id': False}))
#
#     if len(likes) > 0:
#         for like in likes:
#             if email == like['email']:
#                 return jsonify({'msg': '이미 좋아요를 눌렀습니다'})
#         doc = {
#             'num': num_receive,
#             'email': email,
#         }
#         db.likes.insert_one(doc)
#         return jsonify({'msg': '좋아요 완료'})
#
#     doc = {
#         'num': num_receive,
#         'email': email,
#     }
#     db.likes.insert_one(doc)
#     return jsonify({'msg': '좋아요 완료'})
#
# #좋아요 개수 가져오기
# @app.route('/like', methods=["GET"])
# def get_like():
#     likes = list(db.likes.find({}, {'_id': False}))
#     print(len(likes))
#     return jsonify({'likes': likes})
#########################임시###############################


#회원가입 페이지
@app.route("/sign", methods=["GET"])
def join_get():
    return '회원가입 페이지'


#회원 가입
@app.route("/sign", methods=["POST"])
def join_post():
    email_receive = request.form['email_give']
    passwd_receive = request.form['pw_give']
    name_receive = request.form['nick_give']
    lang_receive = request.form['lang_give']
    blog_url_receive = request.form['blog_give']

    member_list = list(db.members.find({}, {'_id': False}))

    for member in member_list:
        if member['email'] == email_receive:
            return jsonify({'msg' :"이미 가입이 완료된 이메일입니다."})



    if email_receive == "" or passwd_receive == "" or name_receive == "" or lang_receive == "" or blog_url_receive =="":
        return jsonify({'msg' :"필수값을 입력해주세요"})

    doc = {
        'email': email_receive,
        'passwd': passwd_receive,
        'name': name_receive,
        'lang': lang_receive,
        'blog_url': blog_url_receive
    }
    db.members.insert_one(doc)

    # 신규가입시 기존 게시글 read 테이블에 추가함
    postings = list(db.postings.find({}, {'_id': False}))

    for posting in postings:
        doc = {
            'num': posting['num'],
            'content': posting['content'],
            'email': email_receive,
            'read': 0
        }
        db.read.insert_one(doc)

    return jsonify({'msg': '가입 완료'})


#로그인 페이지
@app.route("/login", methods=["GET"])
def login_get():
    return "로그인 페이지"

#로그인
@app.route("/login", methods=['POST'])
def login_post():
    email_receive = request.form['loginEmail_give']
    passwd_receive = request.form['loginPw_give']

    login_member = db.members.find_one({"email": email_receive})

    # 이메일이 DB에 없을 때
    if login_member == None:
        return jsonify({'msg' :'존재하지 않는 이메일입니다.'})

    if login_member['passwd'] == passwd_receive:
        response = make_response()
        response.set_cookie('emailCookie', login_member['email'])
        return response
    else:
        # 비밀번호/이메일이 올바르지 않을 때
        return jsonify({'msg' : '비밀번호/이메일이 올바르지 않습니다.'})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)

