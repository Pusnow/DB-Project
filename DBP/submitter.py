#-*- coding:utf-8 -*-

from flask import Flask, request, url_for, abort, render_template, jsonify, session,redirect
from DBP import app
from DBP.models.user import User
from DBP.models.task import Task
from datetime import datetime

ALLOWED_EXTENSIONS = set(['csv'])


@app.route('/submitter/tasks', methods=["GET"])
@app.route('/submitter/tasks/<int:start>/<int:end>', methods=["GET"])
def sbtasks(start = 0, end = 10):
	tasklist = Task.getTasks(start,end)
	return jsonify({"tasks" : map(lambda x : x.dict(),tasklist)})
	
@app.route('/submitter/task', methods=["POST"])
def sbtask():
	data = request.get_json()
	task = Task.getTask(data["prefix"])
	user = User.getUser(session["userid"])
	if task :
		json = task.dict()
		status = task.checkUserStatus(session["userid"])
		json["originals"] =  map(lambda x : x.dict(),task.getOriginals())
		json["originalnum"] = len(json["originals"] )
		json["enrolled"] = task.checkUser(session["userid"])
		json["status"] = status
		json["parsednum"] = task.getParsedNumBySubmitter(user)
		json["submitok"] = (status == "Approved")
		return jsonify({"code" : "success", "task" : json})
	else :
		return jsonify({"code" : "err", "msg" : "No task"})





@app.route('/submitter/applytask', methods=["POST"])
def sbapply():
	data = request.get_json()
	task = Task.getTask(data["prefix"])
	user = User.getUser(session["userid"])



	if task :
		task.addUser(user)
		json = task.dict()
		json["originals"] =  map(lambda x : x.dict(),task.getOriginals())
		json["originalnum"] = len(json["originals"] )
		json["enrolled"] = task.checkUser(session["userid"])
		return jsonify({"code" : "success", "task" : json})
	else :
		return jsonify({"code" : "err", "msg" : "No task"})



@app.route('/submitter/submit', methods=["GET"])
@app.route('/submitter/submit/<int:start>/<int:end>', methods=["GET"])
def sbsubmit(start = 0, end = 10):
	user = User.getUser(session["userid"])

	return jsonify({"tasks" : user.enrollStatus() })


@app.route('/submitter/statistics', methods=["GET"])
def sbgetinfo():
	user = User.getUser(session["userid"])
	return jsonify( {"user" : user.getSubmitInfo() })




@app.route('/submitter/original', methods=["POST"])
def sboriginal():
	data = request.get_json()
	task = Task.getTask(data["prefix"])
	user = User.getUser(session["userid"])
	original = task.getOriginal(data["id"])

	if task :
		json = original.getInfoByUser(user)
		return jsonify({"code" : "success", "original" : json})
	else :
		return jsonify({"code" : "err", "msg" : "No task"})




@app.route('/submitter/submitoriginal', methods=["POST"])
def sbsubmitoriginal():
	data = request.form
	task = Task.getTask(data["prefix"])
	user = User.getUser(session["userid"])
	original = task.getOriginal(data["id"])

	csv = request.files["file"].stream

	original.loadcsv(user,csv,original.getNextnth(user),datetime(2015, 1, 1),datetime(2016, 1, 1))

	return ""



@app.route('/submitter/parsed', methods=["POST"])
def sbparsedlist():
	data = request.get_json()
	task = Task.getTask(data["prefix"])
	user = User.getUser(session["userid"])
	parsedlist = task.getParsedBySubmitter(user)
	if task :
		return jsonify({"code" : "success", "parsedlist" : map(lambda x : x.dict(),parsedlist)})
	else :
		return jsonify({"code" : "err", "msg" : "No task"})



	