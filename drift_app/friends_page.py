import logging
import flask
import flask_login
from flask_login import current_user
from flask import Blueprint, current_app, jsonify, request
from drift_app.db_interface import db_user
import json

friends_bp = Blueprint('friends_bp', __name__)


@friends_bp.route('/friends')
def friends():
    logging.debug(current_user.is_anonymous)
    if flask_login.current_user.is_anonymous:
        return flask.redirect(flask.url_for('login_bp.login'))
    return current_app.send_static_file('react/friends.html')

@friends_bp.route('/get_friend_detail',methods=['POST','GET'])
def get_friend_detail():

    friends=[]
    for i in range(0,6):
        friend = {
            'id':i,
            'friend_account': "xlm%s"%(i),
            'friend_name': 'ssss',
            'avatar': '/static/react/small_avatar.jpg'
        }
        friends.append(friend)

    if request.method=='POST':
        data=request.get_json()
        user_account=data['account']
    else:
        user_account=flask_login.current_user.id
    user_information=json.loads(db_user.get_user_infos(user_account))
    user_information['account']=user_account
    user_information['tags']=db_user.get_user_interests(db_user.get_id_by_account(user_account))
    user_information['following_number']=db_user.get_following(db_user.get_id_by_account(user_account))
    user_information['followers_number']=db_user.get_followers(db_user.get_id_by_account(user_account))

    user_information['pic_src']='/static/react/small_avatar.jpg'
    return jsonify({'user_info':user_information,
                    'friends_list':friends})

@friends_bp.route('/get_friends_list',methods=['POST','GET'])
def get_friends_list():
    if request.method!='POST':
        return 'need POST'
    data=request.get_json()

    user_account=data['account']
    friends=[]
    if data['type']=='following':
        friends=db_user.get_following(db_user.get_id_by_account(user_account))
    elif data['type']=='followers':
        friends=db_user.get_followers(db_user.get_id_by_account(user_account))
    else:
        logging.info('no_type')
        return
    friends_info=[]
    user_information=json.loads(db_user.get_user_infos(data['account']))
    user_information['account']=data['account']
    user_information['pic_src'] = '/static/react/small_avatar.jpg'
    logging.debug("get data %s"%(user_information))
    return jsonify(user_information)