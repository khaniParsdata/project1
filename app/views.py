import json
from threading import current_thread
import flask
import pymssql
from flask import jsonify, request
import jwt
from flask_jwt_extended import (
    create_access_token, create_refresh_token,
    get_jwt_identity, 
    jwt_required, current_user, 
)

from . import models

from . import app # app is in "__init__"



# from os import getenv
# import pymssql

# server = getenv("PYMSSQL_TEST_SERVER")
# user = getenv("PYMSSQL_TEST_USERNAME")
# password = getenv("PYMSSQL_TEST_PASSWORD")

# conn = pymssql.connect(server, user, password, "tempdb")




DB = pymssql.connect(host='localhost', user='SA', password="Fdsa@1234", database="parsdata1")
cursor = DB.cursor()  # use_async_io=True

# cursor.execute('exec first_try')  # this is stored procedure in sql server bash
# row = cursor.fetchall()  
# row = cursor.fetchone()['str']
# row = cursor.fetchone()['uniqueidentifier']


"""
stored procedure:
    get_by_name(1), 
    get_by_id(1), 
    set_profile(4), 
    get_all_users,
    get_by_username,
    change_profile,
"""

# @jwt.user_identity_loader
# def user_identity_lookup(user):
#     return user.id


# @jwt.user_lookup_loader
# def user_lookup_callback(_jwt_header, jwt_data):
#     identity = jwt_data["sub"]
#     return User.query.filter_by(id=identity).one_or_none()


@app.route('/')
def index():
    # return str(row)
    return 'index'


@app.route('/login/', methods=["POST"])
def login():
    username = request.json.get('username', None)
    password = request.json.get('password', None)
    # get user pass from database
    if username is None or password is None:
        return jsonify({"error": "define username and password"})
    
    cursor.execute("exec get_by_username @Username='{}'".format(username))
    result = cursor.fetchall()[0]

    if username != result[3] or password != result[4]:
        return jsonify({"error": "username or password is rong"})
    
    access_token = create_access_token(identity=username, fresh=True)
    refresh_token = create_refresh_token(identity=username)
    return jsonify(access_token=access_token, refresh_token=refresh_token)


@app.route("/refresh_token/", methods=["POST"])
@jwt_required(refresh=True)
def refresh_token():
    username_token = get_jwt_identity()
    access_token = create_access_token(identity=username_token, fresh=False)
    return jsonify(access_token=access_token)


@app.route('/get_profile/<string:name>/', methods=['GET'])
# @jwt_required()
def get_profile(name):
    cursor.execute("exec get_by_name @Name='{}'".format(name))
    result = cursor.fetchall()

    if not len(result):
        return 'not find name'

    return jsonify({"result":
        {"id":result[0][0], "firstName":result[0][1], "lastName":result[0][2]}
    })



@app.route('/set_profile/', methods=['POST'])
@jwt_required()
def set_profile():
    data = request.get_json()
    firstName, lastName, username, password = data["firstName"], data['lastName'], data['username'], data['password']
    if not firstName or not lastName or not username or not password:
        return jsonify({'error': 'should pass all firstName, lastName, username and password'})
    
    username_token = get_jwt_identity()
    
    cursor.execute("exec get_by_username @Username='{}'".format(username_token))
    user_id = cursor.fetchall()[0][0]

    cursor.execute(
        "change_profile @Id='{}', @firstName='{}', @LastName='{}', @username={}, @password={}".format(user_id, firstName, lastName, username, password)
        )
    DB.commit()
    cursor.execute("exec get_by_username @Username='{}'".format(username))
    result = cursor.fetchall()
    # DB.close()
    # cursor.close()
    return jsonify({"new_result":
        {"id":result[0][0], "firstName":result[0][1], "lastName":result[0][2]}
    })


@app.route('/test/', methods=['GET'])
@jwt_required()
def test():
    current_identity = get_jwt_identity()   # return the username of token user
    if current_identity:
        return jsonify(logged_in_as=current_identity)
    else:
        return jsonify(logged_in_ass="anonymous user")
