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

@friends_bp.route('/get_friends_data')
def get_friends_data():
    if flask_login.current_user.is_anonymous:
        return flask.redirect(flask.url_for('login_bp.login'))

    friends=[]
    for i in range(0,6):
        friend = {
            'id':i,
            'friend_account': "xlm%s"%(i),
            'friend_name': 'ssss',
            'avatar': '/static/react/small_avatar.jpg'
        }
        friends.append(friend)
    user_information=json.loads(db_user.get_user_infos(flask_login.current_user.id))
    user_information['account']=flask_login.current_user.id
    user_information['pic_src']='/static/react/small_avatar.jpg'
    jsondata={
        'friends_list':friends,
        'user_info':user_information
    }
    return jsonify(jsondata)

@friends_bp.route('/friend_detail',methods=['POST','GET'])
def friend_detail():
    if request.method!='POST':
        return 'need POST'
    data=request.get_json()
    user_information=json.loads(db_user.get_user_infos(data['account']))
    user_information['account']=data['account']
    user_information['pic_src'] = '/static/react/small_avatar.jpg'
    logging.debug("get data %s"%(user_information))
    return jsonify(user_information)