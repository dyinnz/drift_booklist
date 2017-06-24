import flask
import json
import logging
from flask import Blueprint,jsonify,render_template
from flask import request
import drift_app.db_interface.db_book as db_book
import drift_app.db_interface.db_user_remark as db_user_remark
import flask_login

mine_bp = Blueprint('mine_bp',__name__)

def get_booklist_detail(booklist_id):
    jsondata = {}
    '''
    get booklistdetail by booklist_id
    '''
    books = db_book.get_books_in_booklist(booklist_id)  # 书单id 列表
    booklist = []
    for book in books:  # 获取书单中书籍简要信息
        bookinfo = db_book.get_book(book)
        bookinfo_to_list = {
            'book_id': bookinfo['book_id'],
            'book_name': bookinfo['book_name'],
            'book_cover': bookinfo['book_cover'],
            'author': bookinfo['author'],
            'publisher': bookinfo['publisher']
        }
        booklist.append(bookinfo_to_list)

    vote_number = json.loads(db_user_remark.get_booklist_vote(booklist_id))
    jsondata['up_number'] = vote_number['up']
    jsondata['down_number'] = vote_number['down']
    jsondata['book_number'] = len(books)
    # jsondata['follower_number']=db_user_remark.get_booklist_follower_num(data['booklist_id'])
    # jsondata['remark_number']=db_user_remark.get_booklist_remark_number(data['booklist_id'])
    jsondata['remarks'] = db_user_remark.get_booklist_remark(booklist_id, 1, 10)
    jsondata['booklist'] = booklist
    jsondata['tags'] = db_book.get_booklist_tag(booklist_id)

    return jsondata  #返回字典

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
    '''
    user_id=flask_login.current_user.db_id

    jsondata=get_booklist_detail('my followerd book')

    get my booklist
    get follower booklist
    '''
    jsondata={
        'booklist_id':'id',
        'booklist_cover':'cover',
        'booklist_name':'name',
        'create_user':'username',
        'up_number':1000,
        'down_number':1000,
        'book_number':1000,
        'follower_number':1000,
        'remark_number':1000,
        'tags':['tag1','tag2','tag3'],
        'remarks':['remark1','remark2','remark2'],
        'introduce':'this is introduce',
        'booklist':[{
            'book_id':'bookid',
            'book_name':'bookname',
            'book_cover':'cover',
            'author':'xlm',
            'publisher':'publisher',
        }],
        'my_booklist':[{

        }],
        'follower_booklist':[]
    }
    return   jsonify(jsondata)

@mine_bp.route('/new_booklist',methods=['POST','GET'])
def new_booklist():
    if request.method!='POST':
        return 'need post request'
    data=json.loads(request.get_json())
    user_id=flask_login.current_user.db_id
    new_booklist_id=db_book.add_booklist(user_id,data['booklist_name'],data['booklist_introduce'])
    jsondata=get_booklist_detail(new_booklist_id)
    '''
    get my_booklist
    jsondata['my_booklist']=my_booklist
    '''
    return 'my_booklist'

@mine_bp.route('/booklist_detail',methods=['POST','GET'])
def booklistdetail():
    if request.method=='POST':
        data=json.loads(request.get_json())
        logging.debug(data['booklist_id'])
        jsondata=get_booklist_detail(data['booklist_id'])

        return jsonify(jsondata)
    else:
        return 'need post request'

@mine_bp.route('/book_detail',methods=['POST','GET'])
def bookdetail():
    if request.method!='POST':
        return 'need POST'
    data=json.loads(request.get_json())
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
            user_id = flask_login.current_user.id

    data=json.loads(request.get_json())
    true=db_user_remark.user_remark_booklist(data['booklist_id'],user_id,data['remark'])
    remarks=db_user_remark.get_booklist_remark(data['booklist_id'],1,10)

    return jsonify({'OK':true,'remarks':remarks})

@mine_bp.route('/add_book_remark',methods=['POST','GET'])
def add_book_remark():
    if request.method!='POST':
        return 'need POST'
    else:
        if flask_login.current_user.is_anonymous:
            return flask.redirect(flask.url_for('login_bp.login'))
        else:
            user_id = flask_login.current_user.id

    data=json.loads(request.get_json())
    true=db_user_remark.user_remark_book(data['book_id'],user_id,data['remark'])
    remarks=db_user_remark.get_book_remark(data['book_id'],1,10)
    return jsonify({'OK':true,'remarks':remarks})

@mine_bp.route('/add_to',methods=['POST','GET'])
def add_to():
    if request.method!='POST':
        return 'need POST'
    else:
        if flask_login.current_user.is_anonymous:
            return flask.redirect(flask.url_for('login_bp.login'))

        user_id = flask_login.current_user.db_id
        '''
        get my booklist by user_id
        '''
    return 'my_booklist'

@mine_bp.route('/add_to_list',methods=['POST','GET'])
def add_to_list():
    data=json.loads(request.get_json())
    true=db_book.add_book_to_booklist(data['booklist_id'],['book_id'])

    return jsonify({'OK',true})

@mine_bp.route('/vote_book',methods=['POST','GET'])
def vote_book():
    if request.method!='POST':
        return 'need POST'
    else:
        if flask_login.current_user.is_anonymous:
            return flask.redirect(flask.url_for('login_bp.login'))
        else:
            user_id = flask_login.current_user.db_id

    data=json.loads(request.get_json())
    current_vote=db_user_remark.get_user_book_opinion(user_id,data['book_id'])
    if data['attitude']==current_vote:
        '''
        change attitude to neutral
        '''
    else:
        '''
        change attitude to data['attitude']
        '''
    jsondata={
        'OK':True,
        'attitude':'attitude'
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

    data=json.loads(request.get_json())
    current_vote=db_user_remark.get_user_booklist_opinion(user_id,data['booklist_id'])
    if data['attitude']==current_vote:
        '''
        change attitude to neutral
        '''
    else:
        '''
        change attitude to data['attitude']
        '''
    jsondata={
        'OK':True,
        'attitude':'attitude'
    }
    return jsonify(jsondata)
