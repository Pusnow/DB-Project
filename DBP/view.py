#-*- coding:utf-8 -*-

from flask import Flask, request, url_for, abort, render_template, jsonify, session,redirect
from DBP import app
from DBP.models.user import User
from DBP.models.task import Task



@app.route('/', methods=["GET"])
def index():
	if "logged_in" in session and session['logged_in']:
		user = User.getUser(session['userid'])
		if user.role == u"관리자":
			return render_template('admin.html')

		elif user.role == u"제출자":
			return render_template('submitter.html')
		elif user.role == u"평가자":
			return render_template('evaluator.html')

	return render_template('home.html')



@app.route('/login', methods=["POST"])
def login():

	data = request.get_json()
	if "loginid" not in data or "password" not in data :
		session['logged_in'] = False
		abort(401)
		return jsonify(dict(msg=u"정보가 일치하지 않습니다."))


	if "logged_in" in session and session['logged_in']:
		session['logged_in'] = True
		return jsonify(dict(msg=u"이미 로그인 되어 있습니다."))


	user = User.login(data['loginid'],data['password'])

	if user :
		session['logged_in'] = True
		session['userid'] = user.id
		return jsonify(dict(name = user.name, loginid = user.loginid,msg=u"로그인 성공"))

	else :
		session['logged_in'] = False
		abort(401)
		#return jsonify(dict(msg=u"정보가 일치하지 않습니다."))

@app.route('/logout', methods=["POST"])
def logout():

	session['logged_in'] = False

	session['userid'] = None

	return redirect(url_for('index'))



from DBP import admin
from DBP import submitter
from DBP import evaluator
from DBP import user