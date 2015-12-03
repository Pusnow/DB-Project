
from flask import session



class login(Resource):
	def get(self, loginid, password):
		if session['logged_in']:
		return jsonify(dict(msg=u"이미 로그인 되어 있습니다."))


		print data['loginid'],data['password']
		user = User.login(data['loginid'],data['password'])

		if user :
				session['logged_in'] = True
				session['userid'] = user.id
				return dict(name = user.name, loginid = user.loginid,msg=u"로그인 성공")

		else :
				session['logged_in'] = False
			return dict(msg=u"정보가 일치하지 않습니다.")

