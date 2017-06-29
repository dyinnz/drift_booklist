import logging
import flask
import flask_login
from flask_login import current_user
from flask import Blueprint, current_app, jsonify, request
from drift_app.db_interface import db_user
import json

friends_bp = Blueprint('friends_bp', __name__)

def get_friends_list_by_userid(user_id,ing_or_ers):
    if ing_or_ers=='following':
        friends=json.loads(db_user.get_following(user_id))
    elif ing_or_ers=='followers':
        friends=json.loads(db_user.get_followers(user_id))
    friends_info=[]
    for friend in friends:
        friend_data=json.loads(db_user.get_user_infos(friend[1]))
        friend_info={
            'name':friend_data['name'],
            'avatar':friend_data['pic_src'],
            'account':friend[1],
            'following_number':len(json.loads(db_user.get_following(friend[0]))),
            'followers_number':len(json.loads(db_user.get_followers(friend[0])))
        }
        friends_info.append(friend_info)

    return friends_info

#---------------------------------------------------
@friends_bp.route('/friends')
def friends():
    logging.debug(current_user.is_anonymous)
    if flask_login.current_user.is_anonymous:
        return flask.redirect(flask.url_for('login_bp.login'))
    return current_app.send_static_file('react/friends.html')


@friends_bp.route('/get_friend_detail',methods=['POST','GET'])
def get_friend_detail():
    if request.method=='POST':
        data=request.get_json()
        user_account=data['account']
    else:
        user_account=flask_login.current_user.id
    user_information=json.loads(db_user.get_user_infos(user_account))
    user_information['account']=user_account
    user_information['tags']=json.loads(db_user.get_user_interests(db_user.get_id_by_account(user_account)))
    user_information['following_number']=len(json.loads(db_user.get_following(db_user.get_id_by_account(user_account))))
    user_information['followers_number']=len(json.loads(db_user.get_followers(db_user.get_id_by_account(user_account))))

    return jsonify(user_information)

@friends_bp.route('/get_friends_list',methods=['POST','GET'])
def get_friends_list():
    if request.method!='POST':
        return 'need post request'

    data=request.get_json()
    friends_info=get_friends_list_by_userid(db_user.get_id_by_account(data['account']),data['type'])
    return jsonify(friends_info)
