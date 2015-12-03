#-*- coding:utf-8 -*-

from flask import Flask, request, url_for, abort, render_template, jsonify, session
from DBP import app
from DBP.models.user import User
from DBP.models.task import Task



@app.route('/', methods=["GET"])
def index():
	if "logged_in" in session and session['logged_in']:
		return render_template('admin.html')

	return render_template('home.html')



@app.route('/login', methods=["POST"])
def login():

	data = request.get_json()
	if "logged_in" not in session  or  "loginid" not in data or "password" not in data :
		session['logged_in'] = False
		abort(401)
		return jsonify(dict(msg=u"정보가 일치하지 않습니다."))


	if session['logged_in']:
		session['logged_in'] = True
		return jsonify(dict(msg=u"이미 로그인 되어 있습니다."))


	print data['loginid'],data['password']
	user = User.login(data['loginid'],data['password'])

	if user :
		session['logged_in'] = True
		session['userid'] = user.id
		return jsonify(dict(name = user.name, loginid = user.loginid,msg=u"로그인 성공"))

	else :
		session['logged_in'] = False
		abort(401)
		#return jsonify(dict(msg=u"정보가 일치하지 않습니다."))





@app.route('/admin/tasks', methods=["GET"])
@app.route('/admin/tasks/<int:start>/<int:end>', methods=["GET"])
def tasks(start = 0, end = 10):
	tasklist = Task.getTasks(start,end)
	return jsonify({"tasks" : map(lambda x : x.dict(),tasklist)})
	


@app.route('/admin/users', methods=["GET"])
def users():
	userlist = User.getUsers()
	return jsonify({"users" : map(lambda x : x.dict(),userlist)})


	