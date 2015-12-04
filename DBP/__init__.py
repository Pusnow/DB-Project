#-*- coding:utf-8 -*-
from flask import Flask
from flask_restful import Api
from flask.ext.triangle import Triangle
app = Flask(__name__)
api = Api(app)
Triangle(app)


SECRET_KEY = 'development key'


app.config.from_object(__name__)

app.debug = True
app.config.from_envvar('FLASKR_SETTINGS', silent=True)
app.config['SECRET_KEY']  = SECRET_KEY


import DBP.view