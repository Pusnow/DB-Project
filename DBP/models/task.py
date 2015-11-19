#-*- coding: utf-8 -*-


from DBP.models import Base
from sqlalchemy import Column,  Unicode, Text, DateTime
from sqlalchemy.orm import relationship

class Task(Base):
	__tablename__ = 'Task'
	name = Column(Unicode(100),primary_key = True)
	information = Column(Text)
	duration = Column(DateTime)
	prefix = Column(Unicode(10), unique = True)
