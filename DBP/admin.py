#-*- coding:utf-8 -*-

from flask import Flask, request, url_for, abort, render_template, jsonify, session,redirect,send_file
from DBP import app
from DBP.models.user import User
from DBP.models.task import Task



@app.route('/admin/tasks', methods=["GET"])
@app.route('/admin/tasks/<int:start>/<int:end>', methods=["GET"])
def tasks(start = 0, end = 10):
	tasklist = Task.getTasks(start,end)
	return jsonify({"tasks" : map(lambda x : x.dict(),tasklist)})
	


@app.route('/admin/newuser', methods=["POST"])
def newuser():
	data = request.get_json()
	user = User.newUser(data["loginid"], data["password"], data["name"],data["gender"],data["address"],data["role"],data["birth"],data["cellphone"])
	return jsonify({"code" : "success"})



@app.route('/admin/users', methods=["GET"])
def users():
	userlist = User.getUsers()
	return jsonify({"users" : map(lambda x : x.dict(),userlist)})



@app.route('/admin/user', methods=["POST"])
def user():

	data = request.get_json()
	user = User.getUser(data["id"])
	return jsonify({"user" : user.dict()})



@app.route('/admin/newtask', methods=["POST"])
def newtask():

	data = request.get_json()
	msg = Task.checkData(data)

	
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


@app.route('/admin/taskstatus', methods=["POST"])
def taskstatus():
	data = request.get_json()
	task = Task.getTask(data["prefix"])
	if task :
		task.setStatus(data["status"])

		return jsonify({"code" : "success","task" : task.getInfo()})
	else :
		return jsonify({"code" : "err", "msg" : "No task"})

@app.route('/admin/submitters', methods=["POST"])
def submitters():
	data = request.get_json()
	task = Task.getTask(data["prefix"])
	if task :
		return jsonify({"submitters" : task.getSubmitters()})
	else :
		return jsonify({"code" : "err", "msg" : "No task"})

@app.route('/admin/changesubmitterstatus', methods=["POST"])
def changesubmitterstatus():
	data = request.get_json()
	task = Task.getTask(data["prefix"])
	if task :
		task.changeSubmitterStatus(data["id"],data["status"])
		return jsonify({"code" :"success"})
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
		originallist = map(lambda x : x.getInfo(), task.getOriginals())
		return jsonify({"code" : "success", "originallist" : originallist})

	else :
		return jsonify({"code" : "err", "msg" : "No task"})

	return ""



@app.route('/admin/showparseds', methods=["POST"])
def showparseds():

	data = request.get_json()
	task = Task.getTask(data["prefix"]) 

	if task :
		return jsonify({"code" : "success", "parsedlist" : map(lambda x : x.dict(), task.getParseds())})

	else :
		return jsonify({"code" : "err", "msg" : "No task"})

	return ""



@app.route('/admin/showtupples', methods=["POST"])
def showtupples():

	data = request.get_json()
	task = Task.getTask(data["prefix"]) 

	if task :
		tupples = task.getTupples()
		tupples["code"] = "success"
		return jsonify(tupples)

	else :
		return jsonify({"code" : "err", "msg" : "No task"})

	return ""


@app.route('/admin/useredit', methods=["POST"])
def useredit():
	data = request.get_json()
	user = User.getUser(data["id"])

	if "password" in data :
		user.editInfo(name = data["name"],password = data["password"], gender= data["gender"], address= data["address"], birth= data["birth"], cellphone= data["cellphone"])
	else :
		user.editInfo(name = data["name"],password =  "", gender= data["gender"], address= data["address"], birth= data["birth"], cellphone= data["cellphone"])
	return jsonify({"code" : "success"})



@app.route('/admin/gettaskcsv/<string:prefix>', methods=["GET"])
def gettaskcsv(prefix):

	task = Task.getTask(prefix)
	csv = task.getCSV()

	return send_file(csv, attachment_filename="taskdata.csv", as_attachment=True,mimetype="text/csv")














	