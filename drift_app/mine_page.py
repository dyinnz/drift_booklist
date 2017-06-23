import flask
import json
import logging
from flask import Blueprint,jsonify,render_template
from flask import request
import drift_app.db_interface.db_book as db_book
import drift_app.db_interface.db_user_remark as db_user_remark
import flask_login

mine_bp = Blueprint('mine_bp',__name__)


@mine_bp.route('/test')
def test():
    return flask.current_app.send_static_file('mine.html')
'''
@mine_bp.route('/test/data')
def testclick():
    logging.debug('add succes')
    return 'add'
'''
@mine_bp.route('/mine')
def mine():
    if flask_login.current_user.is_anonymous:
        return flask.redirect(flask.url_for('login_bp.login'))
    else:
        return flask.current_app.send_static_file('mine.html')

@mine_bp.route('/get_mydata')
def get_mydata():
    user_id=flask_login.current_user.id
    jsondata={
        'booklist_id':'id',
        'booklist_cover':'cover',
        'booklist_name':'name',
        'create_user':'username',
        'book_number':1000,
        'follower_number':1000,
        #some other data
        'booklist':['book1','book2','book3'],
        'my_booklist':['list1','list2','list3'],
        'follower_booklist':['list1','list2','list3']
    }
    '''
    get my data
    '''
    return   jsonify(jsondata)

@mine_bp.route('/new_booklist',methods=['POST','GET'])
def new_booklist():
    if request.method=='POST':
        return 'new_booklist'
    return  'need post request'

@mine_bp.route('/booklist_detail',methods=['POST','GET'])
def booklistdetail():
    if request.method=='POST':
        booklistname=request.form.get('booklistname')
        booklistinfo={'booklistname':'name','createuser':'user','like':1000,'remark':1000,'label':'babel','introduce':'introduce'}
        bookinfo={'book1':'book1'}
        booklist=[bookinfo]
        booklistinfo['booklist']=booklist

        jsondata=[booklistinfo,booklistname]
        '''
        get detail data
        '''
        return jsonify(jsondata)
    else:
        return 'need post request'

@mine_bp.route('/book_detail',methods=['POST','GET'])
def bookdetail():
    if request.method!='POST':
        return 'need POST'
    else:
        return 'book_detail'


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

@mine_bp.route('/add_to_list',methods=['POST','GET'])
def add_to_list():
    if request.method!='POST':
        return 'need POST'
    else:
        if flask_login.current_user.is_anonymous:
            return flask.redirect(flask.url_for('login_bp.login'))
        else:
            user_id = flask_login.current_user.id

        data=json.loads(request.get_json())
        '''
        add to list
        
        '''
        true = True
    return jsonify({'OK',true})

@mine_bp.route('/vate_book',methods=['POST','GET'])
def vate_book():
    if request.method!='POST':
        return 'need POST'
    else:
        if flask_login.current_user.is_anonymous:
            return flask.redirect(flask.url_for('login_bp.login'))
        else:
            user_id = flask_login.current_user.id

    data=json.loads(request.get_json())
    current_vate=db_user_remark.get_book_vote(data['book_id'],user_id,data['attitude'])
    if data['attitude']==current_vate:
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
    return 'vote_booklist'
