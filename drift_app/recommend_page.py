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
        booklist_ids=db_user_remark.get_recommend_booklists(flask_login.current_user.db_id,8)
        booklist_ids = [int(x) for x in booklist_ids]

    return jsonify(get_booklist_by_id(booklist_ids))


@recommend_bp.route('/recommend/booklist_by_tag',methods=['POST','GET'])
def booklist_by_tag():
    if request.method != 'POST' :
        return jsonify("need post")

    tag=request.get_json()
    logging.info("tag%s"%tag)
    booklist_ids=db_user_remark.get_recommend_booklist_by_tags(flask_login.current_user.db_id,tag['tag'],8)
    logging.info("booklist_ids:%s"%booklist_ids)

    return jsonify(get_booklist_by_id(booklist_ids))

@recommend_bp.route('/get_popular_user')
def get_popular_user():
    accounts=db_user.get_popular_user(5)

    user_infos=[]
    if accounts!=None:
        for account in accounts:
            user_info_temp=json.loads(db_user.get_user_infos(account))
            user_info={
                'account':account,
                'name':user_info_temp['name'],
                'avatar':user_info_temp['pic_src'],
                'follower_number':len(json.loads(db_user.get_followers(db_user.get_id_by_account(account))))
            }
            user_infos.append(user_info)
    logging.info("popular:%s"%user_infos)
    return jsonify(user_infos)

@recommend_bp.route('/recommend/get_tags')
def get_tags_index():
    if not flask_login.current_user.is_anonymous:
        return db_user.get_user_interests(flask_login.current_user.id)
    else:
        return flask.redirect(flask.url_for('login_bp.login'))


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
    logging.debug(result)
    result = [int(x) for x in result]
    return jsonify(result)

@recommend_bp.route('/interest')
def interest():
    return current_app.send_static_file('react/personal.html')

@recommend_bp.route('/interest/get_tag')
def get_tags():
    if flask_login.current_user.is_anonymous:
        return flask.redirect(flask.url_for('login_bp.login'))

    userTaglist=json.loads(db_user.get_user_interests(flask_login.current_user.id))
    if len(userTaglist)==0:
        islogin=0
    else:
        islogin=1
    jsondata={
        'userTaglist':userTaglist,
        'isLogin':islogin,
        #'taglist':list(set(json.loads(db_user.get_all_tags()))-set(userTaglist))
        'taglist':json.loads(db_user.get_all_tags())
    }
    return jsonify(jsondata)

@recommend_bp.route('/interest/commit',methods=['POST','GET'])
def tag_commit():
    data=request.get_json()
    logging.info('data:%s'%data)
    true=db_user.update_user_tags(flask_login.current_user.id,data['taglist'])
    return jsonify({'OK':true})
