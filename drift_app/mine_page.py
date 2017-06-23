import flask
import logging
from flask import Blueprint,jsonify,render_template
from flask import request
from drift_app.db_interface.db_book import get_book
import flask_login

mine_bp = Blueprint('mine_bp',__name__)
'''
with flask.current_app.test_request_context('/booklistdetail', method='POST'):
    assert request.path == '/booklistdetail'
    assert request.method == 'POST'
'''


@mine_bp.route('/test')
def test():
    return flask.current_app.send_static_file('main_test.html')
    #return flask.render_template('mine_test.html')
    #return flask.redirect(flask.url_for('.mine'))

@mine_bp.route('/test/add')
def add_numbers():
    """Add two numbers server side, ridiculous but well..."""
    a = request.args.get('a', 0, type=int)
    b = request.args.get('b', 0, type=int)
    logging.debug('add succes')
    return jsonify(result = a + b)
    #return 'add'

@mine_bp.route('/mine')
def mine():
    if flask_login.current_user.is_anonymous:
        return flask.redirect(flask.url_for('login_bp.login'))
    else:
        account = flask_login.current_user.id

    booklistinfo={'booklistname':'name','createuser':'user','like':1000,'remark':1000,'label':'babel','introduce':'introduce'}
    bookinfo={'book1':'book1'}
    booklist=[bookinfo]
    booklistinfo['booklist']=booklist

    mybooklist={'booklist1':'booklist1'}
    likebooklist={'booklist2':'booklist2'}
    jsondata=[mybooklist,likebooklist,booklistinfo,account]
    '''
    get mine data
    '''
    return   jsonify(jsondata)

@mine_bp.route('/newbooklist',methods=['POST','GET'])
def newbooklist():
    if request.method=='POST':
        return 'addbooklist'
    return  'GET'

@mine_bp.route('/booklistdetail',methods=['POST','GET'])
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

@mine_bp.route('/bookdetail',methods=['POST','GET'])
def bookdetail():
    if request.method!='POST':
        return 'need POST'
    else:
        #bookid=request.form.get('bookid')
        #return get_book(bookid)
        return 'bookdetail'


@mine_bp.route('/addbooklistremark',methods=['POST','GET'])
def addbooklist():
    if request.method!='POST':
        return 'need POST'
    else:
        booklistname=request.form.get('booklistname');
        if flask_login.current_user.is_anonymous:
            return flask.redirect(flask.url_for('login_bp.login'))
        else:
            account = flask_login.current_user.id
        '''
        addremark
        '''
        return jsonify({'OK',True})

@mine_bp.route('/addbookremark',methods=['POST','GET'])
def addbookremark():
    if request.method!='POST':
        return 'need POST'
    else:
        if flask_login.current_user.is_anonymous:
            return flask.redirect(flask.url_for('login_bp.login'))
        else:
            account = flask_login.current_user.id

        bookname=request.form.get('bookname')
        '''
        addremark
        '''
        return jsonify({'OK',True})

@mine_bp.route('/addtolist',methods=['POST','GET'])
def addtolist():
    if request.method!='POST':
        return 'need POST'
    else:
        if flask_login.current_user.is_anonymous:
            return flask.redirect(flask.url_for('login_bp.login'))
        else:
            account = flask_login.current_user.id

        bookname=request.form.get('bookname')
        booklistname=request.form.get('booklistname')

    return jsonify({bookname,booklistname})
