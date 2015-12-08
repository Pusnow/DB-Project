#-*- coding:utf-8 -*-

from flask import Flask, request, url_for, abort, render_template, jsonify, session,redirect
from DBP import app
from DBP.models.user import User
from DBP.models.task import Task
from DBP.view import logout


@app.route('/user/join', methods=["POST"])
def usjoin():
	data = request.get_json()
	user = User.newUser(data["loginid"], data["password"], data["name"],data["gender"],data["address"],data["role"],data["birth"],data["cellphone"])
	return jsonify({"code" : "success"})




@app.route('/user/edit', methods=["POST"])
def usedit():
	data = request.get_json()
	user = User.getUser(session["userid"])

	if "password" in data :
		user.editInfo(name = data["name"],password = data["password"], gender= data["gender"], address= data["address"], birth= data["birth"], cellphone= data["cellphone"])
	else :
		user.editInfo(name = data["name"],password =  "", gender= data["gender"], address= data["address"], birth= data["birth"], cellphone= data["cellphone"])
	return jsonify({"code" : "success"})



@app.route('/user/info', methods=["GET"])
def usinfo():

	user = User.getUser(session["userid"])
	return jsonify({"code" : "success", "user" : user.dict()})


@app.route('/user/delete', methods=["POST"])
def usdelete():

	user = User.getUser(session["userid"])
	User.deleteUser(user)

	return logout()
