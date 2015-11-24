#-*- coding:utf-8 -*-
from DBP import app
from flask import Flask, request, url_for, abort, render_template, jsonify



@app.route('/', methods=["GET"])
def index():

	return render_template('layout.html')