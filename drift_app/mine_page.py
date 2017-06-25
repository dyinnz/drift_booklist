import flask
import json
import logging
from flask import Blueprint,jsonify,render_template
from flask import request
import drift_app.db_interface.db_book as db_book
import drift_app.db_interface.db_user_remark as db_user_remark
import flask_login
from drift_app.db_interface.db_user import register_user

mine_bp = Blueprint('mine_bp',__name__)

def get_booklist_detail(booklist_id):
    booklistinfo=db_book.get_booklist_by_id(booklist_id)
    jsondata=json.loads(booklistinfo)

    book_ids = json.loads(db_book.get_books_in_booklist(booklist_id))  # 书单id 列表
    if book_ids!=None:
        books = []
        for book_id in book_ids:  # 获取书单中书籍简要信息
            bookinfo = json.loads(db_book.get_book(book_id))
            bookinfo_to_list = {
                'book_id': bookinfo['book_id'],
                'book_name': bookinfo['book_name'],
                #'ISBN':bookinfo['ISBN'],
                'book_cover': bookinfo['book_cover'],
                'author': bookinfo['author'],
                'publisher': bookinfo['publisher'],
                #'introduction':bookinfo['introduction']
            }
            books.append(bookinfo_to_list)

    vote_number = json.loads(db_user_remark.get_booklist_vote(booklist_id))
    jsondata['up_number'] = vote_number['up']
    jsondata['down_number'] = vote_number['down']
    jsondata['book_number'] = len(book_ids)
    jsondata['follower_number']=db_user_remark.get_booklist_follower_num(booklist_id)
    jsondata['remark_number']=db_user_remark.get_booklist_remark_num(booklist_id)
    jsondata['remarks'] = json.loads(db_user_remark.get_booklist_remark(booklist_id, 1, 10))
    jsondata['books'] = books
    jsondata['tags'] = json.loads(db_book.get_booklist_tag(booklist_id))


    return jsondata  #返回字典

def get_booklists_by_ids(booklist_ids):
    my_booklists=[]
    for booklist_id in booklist_ids:
        booklist_info=json.loads(db_book.get_booklist_by_id(booklist_id))
        booklist_to_return={
            'booklist_id':booklist_info['booklist_id'],
            'booklist_cover':booklist_info['booklist_cover'],
            'booklist_name':booklist_info['booklist_name'],
            'book_number':len(json.loads(db_book.get_books_in_booklist(booklist_id)))
        }
        my_booklists.append(booklist_to_return)
    return my_booklists

def get_my_booklists():
    booklist_ids=json.loads(db_book.get_user_created_booklist(flask_login.current_user.db_id))
    if len(booklist_ids)==0:
        new_booklist_id=db_book.add_my_favorite_booklist(booklist_id=0, user_id=flask_login.current_user.db_id, booklist_name='my_favorite', introduction='this is my favorite books', cover='this is cover')
        #book_ids=json.loads(db_user_remark.get_books_user_followed(flask_login.current_user.db_id))
        #for book_id in book_ids:
        #    db_book.add_book_to_booklist(0,book_id)
        booklist_ids.insert(0,new_booklist_id)
    return get_booklists_by_ids(booklist_ids)

def get_booklists_followed():
    booklist_ids=json.loads(db_user_remark.get_booklist_user_followed(flask_login.current_user.db_id))
    return get_booklists_by_ids(booklist_ids)

#----------------------------------------------------------
@mine_bp.route('/test')
def test():
    return flask.current_app.send_static_file('mine.html')


@mine_bp.route('/mine')
def mine():
    if flask_login.current_user.is_anonymous:
        return flask.redirect(flask.url_for('login_bp.login'))
    else:
        return flask.current_app.send_static_file('react/mine.html')

@mine_bp.route('/get_mydata',methods=['POST','GET'])
def get_mydata():
    jsondata={
    'my_booklists':get_my_booklists(),
    'followed_booklists':get_booklists_followed()
    }

    return   jsonify(jsondata)

@mine_bp.route('/new_booklist',methods=['POST','GET'])
def new_booklist():
    if request.method!='POST':
        return 'need post request'
    data=request.get_json()
    user_id=flask_login.current_user.db_id
    new_booklist_id=db_book.add_booklist(user_id,data['booklist_name'],data['booklist_introduction'],data['booklist_cover'])
    if new_booklist_id ==None :
        return None
    jsondata=get_booklist_detail(new_booklist_id)

    jsondata['my_booklist']=get_my_booklists()

    return jsonify(jsondata)

@mine_bp.route('/booklist_detail',methods=['POST','GET'])
def booklistdetail():
    if request.method=='POST':
        data=request.get_json()
        jsondata=get_booklist_detail(data['booklist_id'])
        logging.debug(jsondata)
        return jsonify(jsondata)
    else:
        return 'need post request'

@mine_bp.route('/book_detail',methods=['POST','GET'])
def bookdetail():
    if request.method!='POST':
        return 'need POST'
    data=request.get_json()
    jsondata=json.loads(db_book.get_book(data['book_id']))

    jsondata['follower_number']=db_user_remark.get_book_follower_num(data['book_id'])
    vote_number=json.loads(db_user_remark.get_book_vote_num(data['book_id']))
    jsondata['up_number']=vote_number['up']
    jsondata['down_number']=vote_number['down']
    jsondata['remarks']=json.loads(db_user_remark.get_book_remark(data['book_id'],1,10))

    return jsonify(jsondata)

@mine_bp.route('/add_booklist_remark',methods=['POST','GET'])
def add_booklist_remark():
    if request.method!='POST':
        return 'need POST'
    else:
        if flask_login.current_user.is_anonymous:
            return flask.redirect(flask.url_for('login_bp.login'))
        else:
            user_id = flask_login.current_user.db_id

    data=request.get_json()
    true=db_user_remark.user_remark_booklist(data['booklist_id'],user_id,data['remark'])
    remarks=json.loads(db_user_remark.get_booklist_remark(data['booklist_id'],1,10))

    return jsonify({'OK':true,'remarks':remarks})

@mine_bp.route('/add_book_remark',methods=['POST','GET'])
def add_book_remark():
    if request.method!='POST':
        return 'need POST'
    else:
        if flask_login.current_user.is_anonymous:
            return flask.redirect(flask.url_for('login_bp.login'))
        else:
            user_id = flask_login.current_user.db_id

    data=request.get_json()
    true=db_user_remark.user_remark_book(data['book_id'],user_id,data['remark'])
    remarks=json.loads(db_user_remark.get_book_remark(data['book_id'],1,10))
    return jsonify({'OK':true,'remarks':remarks})

@mine_bp.route('/add_to',methods=['POST','GET'])
def add_to():
    if request.method!='POST':
        return 'need POST'
    else:
        if flask_login.current_user.is_anonymous:
            return flask.redirect(flask.url_for('login_bp.login'))

        user_id = flask_login.current_user.db_id
        my_booklist_ids=json.loads(db_book.get_user_created_booklist(user_id))
        booklist_names=[]
        for my_booklist_id in my_booklist_ids:
            booklist_info=json.loads(db_book.get_booklist_by_id(my_booklist_id))
            booklist_names.append((booklist_info['booklist_name'],my_booklist_id))

    return jsonify(booklist_names)

@mine_bp.route('/add_to_list',methods=['POST','GET'])
def add_to_list():
    data=request.get_json()
    true=db_book.add_book_to_booklist(data['booklist_id'],data['book_id'])

    return jsonify({'OK':true})

@mine_bp.route('/vote_book',methods=['POST','GET'])
def vote_book():
    if request.method!='POST':
        return 'need POST'
    else:
        if flask_login.current_user.is_anonymous:
            return flask.redirect(flask.url_for('login_bp.login'))
        else:
            user_id = flask_login.current_user.db_id

    data=request.get_json()
    current_vote=json.loads(db_user_remark.get_user_book_opinion(user_id,data['book_id']))
    true=False
    if data['attitude']==current_vote[0]:
        true=db_user_remark.user_vote_book(data['book_id'],user_id,'netural')
    else:
        true=db_user_remark.user_vote_book(data['book_id'],user_id,data['attitude'])
    jsondata={
        'OK':true,
        'vote':json.loads(db_user_remark.get_user_book_opinion(user_id,data['book_id']))[0]
    }
    return jsonify(jsondata)

@mine_bp.route('/vote_booklist',methods=['POST','GET'])
def vote_booklist():
    if request.method!='POST':
        return 'need POST'
    else:
        if flask_login.current_user.is_anonymous:
            return flask.redirect(flask.url_for('login_bp.login'))
        else:
            user_id = flask_login.current_user.db_id

    data=request.get_json()
    current_vote=json.loads(db_user_remark.get_user_booklist_opinion(user_id,data['booklist_id']))
    true=False
    if data['attitude']==current_vote[0]:
        true=db_user_remark.user_vote_booklist(data['booklist_id'],user_id,'netural')
    else:
        true=db_user_remark.user_vote_booklist(data['booklist_id'],user_id,data['attitude'])
    jsondata={
        'OK':true,
        'vote':json.loads(db_user_remark.get_user_booklist_opinion(user_id,data['booklist_id']))[0]
    }
    return jsonify(jsondata)

@mine_bp.route('/follow_book',methods=['POST','GET'])
def follow_book():
    if request.method!='POST':
        return 'need POST'
    else:
        if flask_login.current_user.is_anonymous:
            return flask.redirect(flask.url_for('login_bp.login'))
        else:
            user_id = flask_login.current_user.db_id
    data=request.get_json()
    current_vate=db_user_remark.get_user_book_opinion(user_id,data['book_id'])
    true=False

    if current_vate is None or json.loads(current_vate)[1]==False:
        true = db_user_remark.set_book_follow(user_id, data['book_id'], True)
    else:
        true = db_user_remark.set_book_follow(user_id, data['book_id'], False)

    return jsonify({'OK': true,
                    'is_follow': json.loads(db_user_remark.get_user_book_opinion(user_id, data['book_id']))[1]
                    })

@mine_bp.route('/follow_booklist',methods=['POST','GET'])
def follow_booklist():
    if request.method!='POST':
        return 'need POST'
    else:
        if flask_login.current_user.is_anonymous:
            return flask.redirect(flask.url_for('login_bp.login'))
        else:
            user_id = flask_login.current_user.db_id
    data=request.get_json()
    true=False
    current_vote=db_user_remark.get_user_booklist_opinion(user_id,data['booklist_id'])

    if current_vote is None or json.loads(current_vote)[1] == False:
        true=db_user_remark.set_booklist_follow(user_id,data['booklist_id'],True)
    else:
        true=db_user_remark.set_booklist_follow(user_id,data['booklist_id'],False)

    return jsonify({'OK':true,
                    'is_follow':json.loads(db_user_remark.get_user_booklist_opinion(user_id,data['booklist_id']))[1]
                    })