from flask import Blueprint, current_app,request ,jsonify
import flask_login
import logging
import json
import flask
from drift_app.db_interface import  db_book
from drift_app.db_interface import db_user_remark
from drift_app.db_interface import db_user

recommend_bp = Blueprint('recommend_bp', __name__)

def get_booklist_by_id(booklist_ids):
    booklist_infos=[]
    for booklist_id in booklist_ids:
        booklist_info=json.loads(db_book.get_booklist_by_id(booklist_id))
        booklist_info['up_number']=json.loads(db_user_remark.get_booklist_vote(booklist_id))['up']
        booklist_info['remark_number']=db_user_remark.get_booklist_remark_num(booklist_id)

        user_info=json.loads(db_user.get_user_infos(booklist_info['create_user']))
        booklist_info['user_account']=booklist_info['create_user']
        booklist_info['avatar']=user_info['pic_src']
        booklist_info['user_name']=user_info['name']

        del booklist_info['create_user']
        del booklist_info['introduction']
        booklist_infos.append(booklist_info)
    return booklist_infos
#-----------------------------------------------------------------------
@recommend_bp.route('/index')
@recommend_bp.route('/recommend')
def recommend():
    if not flask_login.current_user.is_anonymous:
        logging.info('recommend page for %s', flask_login.current_user.get_id())
    else:
        logging.info('recomemnd page for anonymous')
        return flask.redirect(flask.url_for('login_bp.login'))

    return current_app.send_static_file('react/index.html')


@recommend_bp.route('/recommend/fetch')
def recommend_fetch():
    booklist_ids = json.loads(db_book.get_user_created_booklist(flask_login.current_user.db_id))
    if flask_login.current_user.is_anonymous:
        """get booklist Ids"""
    else:
        """get booklist ids"""

    return jsonify(get_booklist_by_id(booklist_ids))

@recommend_bp.route('/recommend/get_tags')
def get_tags():
    if flask_login.current_user.is_anonymous:
        return flask.redirect(flask.url_for('login_bp.login'))
    else:
        return db_user.get_user_interests(flask_login.current_user.db_id)

@recommend_bp.route('/recommend/booklist_by_tag',methods=['POST','GET'])
def booklist_by_tag():
    if request.method != 'POST' :
        return jsonify("need post")

    tag=request.get_json()
    logging.info(tag)
    """get booklist by tag"""
    booklist_ids = json.loads(db_book.get_user_created_booklist(flask_login.current_user.db_id))

    return jsonify(get_booklist_by_id(booklist_ids))

@recommend_bp.route('/get_popular_user')
def get_popular_user():
    accounts=[]
    '''get popular user accounts'''
    accounts=[follower[1] for follower in json.loads(db_user.get_followers(flask_login.current_user.db_id))]

    user_infos=[]
    for account in accounts:
        user_info_temp=json.loads(db_user.get_user_infos(account))
        user_info={
            'account':account,
            'name':user_info_temp['name'],
            'avatar':user_info_temp['pic_src'],
            'follower_number':len(json.loads(db_user.get_followers(db_user.get_id_by_account(account))))
        }
        user_infos.append(user_info)
    return jsonify(user_infos)

@recommend_bp.route('/recommend/islogin')
def islogin():
    jsondata={}
    if flask_login.current_user.is_anonymous:
        jsondata['isLogIn']=0
        jsondata['user_cover']=''
        jsondata['user_name']=''
        return jsonify(jsondata)
    user_data=json.loads(db_user.get_user_infos(flask_login.current_user.id))
    jsondata['isLogIn']=1
    jsondata['user_cover']=user_data['pic_src']
    jsondata['user_name']=user_data['name']
    jsondata['user_account']=flask_login.current_user.id
    return jsonify(jsondata)

@recommend_bp.route('/get_recommend')
def get_recommend():
    result = db_user_remark.get_recommend_booklists(flask_login.current_user.db_id, 10)
    result = [int(x) for x in result]
    logging.debug(result)
    return jsonify(result)