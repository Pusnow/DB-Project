#-*- coding: utf-8 -*-


from DBP.models import Base,session
from sqlalchemy import Column, Integer, Unicode, Enum, Date
from sqlalchemy import Table, ForeignKey, PrimaryKeyConstraint

from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

import random

class Enroll(Base):
	__tablename__ = 'Enroll'
	__table_args__ = (PrimaryKeyConstraint('taskname','userid',name='enroll_pk'),)
	taskname = Column('taskname', Unicode(100), ForeignKey('Task.name'), nullable = False)
	userid = Column('userid', Integer, ForeignKey('User.id'), nullable = False)
	status = Column('status',Enum(u"Waiting",u"Approved",u"Refused"), nullable = False , server_default = "Waiting")

	


class User(Base):
	__tablename__ = 'User'
	id = Column(Integer, primary_key=True, autoincrement = True, nullable = False)
	login = Column(Unicode(100), unique = True, nullable = False)
	password = Column(Unicode(100), nullable = False)
	name = Column(Unicode(100), nullable = False)
	gender = Column(Enum(u"남자", u"여자"), nullable = False, server_default = u"남자")
	address = Column(Unicode(255))
	role = Column(Enum(u"관리자", u"제출자", u"평가자"), nullable = False, server_default =  u"제출자")
	score = Column(Integer, server_default = "0", nullable = False)
	birth = Column(Date)
	cellphone = Column(Unicode(15))

	def __init__(self,login,name,password):
		self.login = login
		self.name = name
		self.password = password


def randomEvaluator():
	maxnum = session.query(func.max(User.id)).filter(User.role == u"평가자").one()[0]
	userid = random.randrange(1,maxnum +1)

	return session.query(User).get(userid)

