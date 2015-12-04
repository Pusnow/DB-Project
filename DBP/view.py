#-*- coding:utf-8 -*-

from flask import Flask, request, url_for, abort, render_template, jsonify, session
from DBP import app
from DBP.models.user import User
from DBP.models.task import Task



@app.route('/', methods=["GET"])
def index():
	if "logged_in" in session and session['logged_in']:
		user = User.getUser(session['userid'])
		if user.role == u"관리자":
			return render_template('admin.html')

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





@app.route('/admin/tasks', methods=["GET"])
@app.route('/admin/tasks/<int:start>/<int:end>', methods=["GET"])
def tasks(start = 0, end = 10):
	tasklist = Task.getTasks(start,end)
	return jsonify({"tasks" : map(lambda x : x.dict(),tasklist)})
	


@app.route('/admin/newuser', methods=["POST"])
def newuser():
	data = request.get_json()
	print data
	user = User.newUser(data["loginid"], data["password"], data["name"],data["gender"],data["address"],data["role"],data["birth"],data["cellphone"])
	return jsonify({"code" : "success"})



@app.route('/admin/users', methods=["GET"])
def users():
	userlist = User.getUsers()
	return jsonify({"users" : map(lambda x : x.dict(),userlist)})


@app.route('/admin/newtask', methods=["POST"])
def newtask():

	data = request.get_json()
	msg = Task.checkData(data)

	print msg
	if not msg == "":
		return jsonify({"code" : "err", "msg" : msg})

	else :
		task = Task.newTask(data)


		return jsonify({"code" : "success", "task" : task.dict()})

@app.route('/admin/task', methods=["POST"])
def task():
	data = request.get_json()
	task = Task.getTask(data["prefix"])
	if task :
		return jsonify({"task" : task.getInfo()})
	else :
		return jsonify({"code" : "err", "msg" : "No task"})




@app.route('/admin/neworiginal', methods=["POST"])
def neworiginal():

	data = request.get_json()
	task = Task.getTask(data["prefix"]) 

	if task :
		msg = Task.checkOriginal(data)
		if msg != "" :
			return jsonify({"code" : "err", "msg" : msg})
		else :
			original = task.newOriginal(data["length"],data["name"],data["schemas"])
			return jsonify({"code" : "success", "task" : original.dict()})

	else :
		return jsonify({"code" : "err", "msg" : "No task"})

	return ""


@app.route('/admin/showoriginals', methods=["POST"])
def showoriginals():

	data = request.get_json()
	task = Task.getTask(data["prefix"]) 

	if task :
		originallist = map(lambda x : x.dict(), task.getOriginals())
		return jsonify({"code" : "success", "originallist" : originallist})

	else :
		return jsonify({"code" : "err", "msg" : "No task"})

	return ""
	