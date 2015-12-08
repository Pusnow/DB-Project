#-*- coding:utf-8 -*-

from flask import Flask, request, url_for, abort, render_template, jsonify, session,redirect, make_response
from DBP import app
from DBP.models.user import User
from DBP.models.task import Task
from datetime import datetime

ALLOWED_EXTENSIONS = set(['csv'])


@app.route('/evaluator/parseds', methods=["GET"])
def evparseds():
	return jsonify({"parsedlist" : Task.getEvaluateReady(session["userid"])})




@app.route('/evaluator/parsedsdone', methods=["GET"])
def evparsedsdone():
	return jsonify({"parsedlist" : Task.getEvaluateDone(session["userid"])})


@app.route('/evaluator/parsed', methods=["POST"])
def evparsed():
	data = request.get_json()

	task = Task.getTask(data["prefix"])

	parsed = task.getParsed(data["id"])




	return jsonify({"parsed" : parsed.dict(), "task" : task.dict()})


	


@app.route('/evaluator/getfile/<string:prefix>/<int:id>', methods=["GET"])
def getfile(prefix,id):
	task = Task.getTask(prefix)

	parsed = task.getParsed(id)

	response = make_response(parsed.file)
	response.headers['Content-type'] = "text/csv"
	response.headers["Content-Disposition"] = "attachment; filename=parsingdatasequence.csv"
	return response




@app.route('/evaluator/submitevaluate', methods=["POST"])
def evsubmitevaluate():
	data = request.get_json()
	task = Task.getTask(data["prefix"])

	parsed = task.getParsed(data["id"])

	if data["pass"]:
		parsed.evaluate(data["score"] , "Pass")
		user = User.getUser(parsed.submitterid).setScore()
		parsed.insertcsv()
	else :
		parsed.evaluate(data["score"] , "Nonpass")


	return jsonify({"code" : "success"})


	

