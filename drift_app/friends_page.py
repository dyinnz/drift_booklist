import json
import logging

import flask
import flask_login
from flask import Blueprint, current_app, jsonify, request
from drift_app.mine_page import get_booklists_by_ids
import drift_app.db_interface.db_user_remark as db_user_remark
import drift_app.db_interface.db_book as db_book

from drift_app.db_interface import db_user

friends_bp = Blueprint('friends_bp', __name__)


def get_friends_list_by_userid(user_id, ing_or_ers):
    if ing_or_ers == 'following':
        friends = json.loads(db_user.get_following(user_id))
    elif ing_or_ers == 'followers':
        friends = json.loads(db_user.get_followers(user_id))
    friends_info = []
    for friend in friends:
        friend_data = json.loads(db_user.get_user_infos(friend[1]))
        friend_info = {
            'name': friend_data['name'],
            'avatar': friend_data['pic_src'],
            'account': friend[1],
            'following_number': len(json.loads(db_user.get_following(friend[0]))),
            'followers_number': len(json.loads(db_user.get_followers(friend[0])))
        }
        friends_info.append(friend_info)

    return friends_info


def get_relationship(user_id):
    if flask_login.current_user.db_id == user_id:
        return 'self'
    following = db_user.user1_follow_user2(flask_login.current_user.db_id, user_id)
    followed = db_user.user1_follow_user2(user_id, flask_login.current_user.db_id)
    if following and followed:
        return '相互关注'
    elif following and not followed:
        return '已关注'
    elif not following and followed:
        return '关注了你'
    else:
        return '点击关注'

def get_information_by_account(user_account):
    user_information = json.loads(db_user.get_user_infos(user_account))
    user_information['account'] = user_account
    user_information['tags'] = json.loads(db_user.get_user_interests(user_account))
    user_information['following_number'] = len(
        json.loads(db_user.get_following(db_user.get_id_by_account(user_account))))
    user_information['followers_number'] = len(
        json.loads(db_user.get_followers(db_user.get_id_by_account(user_account))))
    user_information['relationship']=get_relationship(db_user.get_id_by_account(user_account))

    return user_information

# ---------------------------------------------------
@friends_bp.route('/friends')
def friends():
    if flask_login.current_user.is_anonymous:
        return flask.redirect(flask.url_for('login_bp.login'))
    return current_app.send_static_file('react/friends.html')


@friends_bp.route('/get_friend_detail', methods=['POST', 'GET'])
def get_friend_detail():
    if request.method == 'POST':
        data = request.get_json()
        user_account = data['account']
    else:
        user_account = flask_login.current_user.id

    logging.info("user account %s"%user_account)
    return jsonify(
         get_information_by_account(user_account))

@friends_bp.route('/user/<account>',methods=['POST','GET'])
def user_detail(account):
    if request.method!='POST':
        return current_app.send_static_file('react/friends.html')

    return jsonify(get_information_by_account(account))

@friends_bp.route('/get_friends_list', methods=['POST', 'GET'])
def get_friends_list():
    if request.method != 'POST':
        return jsonify('need post request')

    data = request.get_json()
    friends_info = get_friends_list_by_userid(db_user.get_id_by_account(data['account']), data['type'])
    return jsonify(friends_info)


@friends_bp.route('/follow_user', methods=['POST', 'GET'])
def follow_user():
    if request.method != 'POST':
        return jsonify('need post request')
    if flask_login.current_user.is_anonymous:
        return flask.redirect(flask.url_for('login_bp.login'))

    data = request.get_json()
    user_id = db_user.get_id_by_account(data['account'])
    following = db_user.user1_follow_user2(flask_login.current_user.db_id, user_id)

    if following:
        true = db_user.unfollow_user(flask_login.current_user.db_id, user_id)
    else:
        true = db_user.follow_user(flask_login.current_user.db_id, user_id)

    logging.info("%s,%s,%s" % (get_relationship(user_id), following, user_id))
    return jsonify({
        'OK': true,
    })

@friends_bp.route('/get_user_booklist',methods=['POST','GET'])
def get_user_booklist():
    if request.method!='POST':
        return jsonify('need post')

    data=request.get_json()
    logging.info(data)
    user_id=db_user.get_id_by_account(data['account'])
    booklist_created_ids=json.loads(db_book.get_user_created_booklist(user_id))
    booklist_followed_ids=json.loads(db_user_remark.get_booklist_user_followed(user_id))

    jsondata={
        'booklist_created':get_booklists_by_ids(booklist_created_ids),
        'booklist_followed':get_booklists_by_ids(booklist_followed_ids)
    }
    return jsonify(jsondata)

@friends_bp.route('/get_tags')
def get_tags():
    return db_user.get_all_tags()
