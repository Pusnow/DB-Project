#-*- coding: utf-8 -*-


from DBP.models import Base
from sqlalchemy import Column, Integer, Unicode, Enum, Date
from sqlalchemy import Table, ForeignKey, PrimaryKeyConstraint

from sqlalchemy.orm import relationship




class Enroll(Base):
	__tablename__ = 'Enroll'
	__table_args__ = (PrimaryKeyConstraint('taskname','userid',name='enroll_pk'),)
	taskname = Column('taskname', Unicode(100), ForeignKey('Task.name'), nullable = False)
	userid = Column('userid', Unicode(30), ForeignKey('User.id'), nullable = False)
	status = Column('status',Enum(u"Waiting",u"Approved",u"Refused"), nullable = False , server_default = "Waiting")

	


class User(Base):
	__tablename__ = 'User'
	id = Column(Unicode(30), primary_key=True)
	password = Column(Unicode(100), nullable = False)
	name = Column(Unicode(100), nullable = False)
	gender = Column(Enum(u"남자", u"여자"), nullable = False, server_default = u"남자")
	address = Column(Unicode(255))
	role = Column(Enum(u"관리자", u"제출자", u"평가자"), nullable = False, server_default =  u"제출자")
	score = Column(Integer, server_default = "0", nullable = False)
	birth = Column(Date)
	cellphone = Column(Unicode(15))
