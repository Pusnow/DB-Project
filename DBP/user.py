#-*- coding:utf-8 -*-

from flask import Flask, request, url_for, abort, render_template, jsonify, session,redirect
from DBP import app
from DBP.models.user import User
from DBP.models.task import Task



@app.route('/user/join', methods=["POST"])
def usjoin():
	data = request.get_json()
	user = User.newUser(data["loginid"], data["password"], data["name"],data["gender"],data["address"],data["role"],data["birth"],data["cellphone"])
	return jsonify({"code" : "success"})




@app.route('/user/edit', methods=["POST"])
def usedit():
	data = request.get_json()
	user = User.newUser(data["loginid"], data["password"], data["name"],data["gender"],data["address"],data["role"],data["birth"],data["cellphone"])
	return jsonify({"code" : "success"})



@app.route('/user/info', methods=["GET"])
def usinfo():
	data = request.get_json()
	user = User.newUser(data["loginid"], data["password"], data["name"],data["gender"],data["address"],data["role"],data["birth"],data["cellphone"])
	return jsonify({"code" : "success"})
