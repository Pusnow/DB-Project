#-*- coding: utf-8 -*-


from DBP.models import Base,session
from sqlalchemy import Column, Integer, Unicode, Enum, Date, String
from sqlalchemy import Table, ForeignKey, PrimaryKeyConstraint
from sqlalchemy.sql.expression import label
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime
import random

from werkzeug.security import generate_password_hash, check_password_hash


enrollcode = {
	"Waiting" : u"승인 대기중",
	"Approved" : u"승인 완료",
	"Refused" : u"승인 거절",
}



class Enroll(Base):
	__tablename__ = 'Enroll'
	__table_args__ = (PrimaryKeyConstraint('taskprefix','userid',name='enroll_pk'),)
	taskprefix = Column('taskprefix', Unicode(100), ForeignKey('Task.prefix'), nullable = False)
	userid = Column('userid', Integer, ForeignKey('User.id'), nullable = False)
	status = Column('status',Enum(u"Waiting",u"Approved",u"Refused"), nullable = False , server_default = "Waiting")
	user = relationship("User", backref="enrolls")
	


class User(Base):
	__tablename__ = 'User'
	id = Column(Integer, primary_key=True, autoincrement = True, nullable = False)
	loginid = Column(Unicode(100), unique = True, nullable = False)
	password = Column(String(100), nullable = False)
	name = Column(Unicode(100), nullable = False)
	gender = Column(Enum(u"남자", u"여자"), nullable = False, server_default = u"남자")
	address = Column(Unicode(255))
	role = Column(Enum(u"관리자", u"제출자", u"평가자"), nullable = False, server_default =  u"제출자")
	score = Column(Integer, server_default = "0", nullable = False)
	birth = Column(Date)
	cellphone = Column(Unicode(15))



	def __init__(self,loginid,name,password):
		self.loginid = loginid
		self.name = name
		self.password = generate_password_hash(password)

	def checkPassword(self,password):
		return check_password_hash(self.password, password)


	def dict(self):
		data = {"id" : self.id, 
		"loginid" : self.loginid, 
		"name" : self.name, 
		"gender" : self.gender, 
		"address" : self.address,
		"role" : self.role,
		"score" : self.score,
		"birthstring" : self.birth,
		"cellphone" : self.cellphone
		}
		if data["birthstring"] :
			data["birthstring"] = data["birthstring"].isoformat()


		return data


	def enrollStatus(self):
		enrolls = list()

		for enroll in self.enrolls:
			task = enroll.task.dict()
			task["status"] = enrollcode[enroll.status]
			enrolls.append(task)

		return enrolls

	



	@staticmethod
	def randomEvaluator():
		maxnum = session.query(func.max(User.id)).filter(User.role == u"평가자").one()[0]
		userid = random.randrange(1,maxnum +1)

		return session.query(User).get(userid)

	@staticmethod
	def getUser(id):
		return session.query(User).get(id)


	@staticmethod
	def getUsers():
		return session.query(User).order_by(User.id).all()

	@staticmethod
	def newUser(loginid, password, name, gender, address , role, birth,cellphone):
		user = User(loginid, name, password)
		user.gender = gender
		user.address = address
		user.role = role
		user.birth = datetime.strptime(birth, "%a, %d %b %Y %H:%M:%S %Z").date()
		user.cellphone = cellphone
		session.add(user)
		session.commit()


	@staticmethod
	def login(loginid, password):
		
		user = session.query(User).filter(User.loginid == loginid).first()

		if user and user.checkPassword(password) :
			return user
		else :
			return None





