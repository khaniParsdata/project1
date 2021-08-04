from flask import Flask

import pymssql

from flask_jwt_extended import JWTManager

app = Flask(__name__, instance_relative_config=True)

from . import views

app.config.from_object('config')
# app.config.from_pyfile('config.py')

jwt = JWTManager(app)


# import db engin
