#-*- coding: utf-8 -*-

from DBP.models import Base, engine, session
from sqlalchemy import Column,  Unicode, Text, DateTime, Integer, BLOB, ForeignKey, Enum
from sqlalchemy.orm import relationship, relation
from sqlalchemy import Table, MetaData
from DBP.models.instance import OriginalData, TaskData, ParsedData
from sqlalchemy.orm import mapper
from DBP.models.user import User,Enroll

import re


class Task(Base):
	__tablename__ = 'Task'
	prefix = Column(Unicode(10), primary_key = True)
	name = Column(Unicode(100), nullable = False)
	information = Column(Text)
	duration = Column(Integer, nullable = False)


	enroll = relationship("Enroll",lazy='dynamic', backref= "task")


	def __init__(self,name,duration,prefix):
		self.name = name[:100]
		self.duration = duration
		self.prefix = prefix[:10]



	def setTables(self):
		metadata = Base.metadata
		originalTableName = self.prefix + "_OriginalData"
		parsedTableName = self.prefix + "_ParsedData"
		taskTableName = self.prefix + "_TaskData"
		self.originaltable = Table(originalTableName, metadata, autoload=True, autoload_with=engine)
		self.parsedtable = Table(parsedTableName, metadata, autoload=True, autoload_with=engine)
		self.tasktable = Table(taskTableName, metadata, autoload=True, autoload_with=engine)

		self.original = type(str(originalTableName),(OriginalData,),{})
		self.parsed = type(str(parsedTableName),(ParsedData,),{})
		self.task = type(str(taskTableName),(TaskData,),{})
		mapper(self.original, self.originaltable, properties={
			'parseds': relationship(self.parsed, backref='original')
		})
		mapper(self.parsed, self.parsedtable, properties={
			'tasks': relationship(self.task, backref='parsed')
		})
		mapper(self.task, self.tasktable)

		self.original.parsedclass = self.parsed
		self.parsed.taskclass = self.task



	def generateTables(self,mappinginfo):
		metadata = Base.metadata
		#original data


		originalTableName = self.prefix + "_OriginalData"
		self.originaltable = Table(originalTableName,metadata,
			Column('id', Integer, primary_key=True,autoincrement = True),
			Column('length', Integer),
			Column('name', Unicode(100)),
			*(Column("sch_"+colname, Integer) for colname in mappinginfo)
			#,autoload=True, autoload_with=engine
			)

		#parsed data
		parsedTableName = self.prefix + "_ParsedData"




		self.parsedtable = Table(parsedTableName,metadata,
			Column('id', Integer, primary_key=True,autoincrement = True),
			Column('duration_start', DateTime, nullable = False),
			Column('duration_end', DateTime, nullable = False),
			Column('nth', Integer, nullable = False, server_default = "1"),
			Column('file',BLOB, nullable = False),
			Column('tuplenum',Integer, nullable = False),
			Column('duplicatetuplenum',Integer, nullable = False),
			Column('originalid', Integer, ForeignKey(originalTableName+'.id'), nullable = False),
			Column('evaluatorid', Integer, ForeignKey('User.id'),  nullable = False),
			Column('status',Enum('Waiting','Evaluated'), nullable = False, server_default = 'Waiting'),
			Column('score',Integer, nullable = False, server_default= "0"),
			Column('pnp',Enum('Pass','Nonpass'), nullable = False, server_default = 'Nonpass'),
			Column('submitterid', Integer, ForeignKey('User.id'), nullable = False)
			#,autoload=True, autoload_with=engine
			)


		#task data
		
		taskTableName = self.prefix + "_TaskData"
		self.tasktable = Table(taskTableName,metadata,
			Column('id', Integer, primary_key=True,autoincrement = True),
			Column('submittername', Unicode(100), nullable = False),
			Column('parsedid', Integer, ForeignKey(parsedTableName+'.id'), nullable = False),
			*(Column("sch_"+colname, Unicode(100)) for colname in mappinginfo)
			#,autoload=True, autoload_with=engine
			)

		metadata.create_all(bind= engine)



		self.original = type(str(originalTableName),(OriginalData,),{})
		self.parsed = type(str(parsedTableName),(ParsedData,),{})
		self.task = type(str(taskTableName),(TaskData,),{})
		mapper(self.original, self.originaltable)
		mapper(self.parsed, self.parsedtable, properties={
			'original': relationship(self.original, backref='parsed')
		})
		mapper(self.task, self.tasktable, properties={
			'parsed': relationship(self.parsed, backref='task'),
		})

		self.original.parsedclass = self.parsed
		self.parsed.taskclass = self.task

		return True



	def newOriginal(self, length, name,mappinginfo):
		originalmodel = self.original(length, name,mappinginfo)
		session.add(originalmodel)
		session.commit()
		return originalmodel



	def getMapInfo(self):
		info = list()
		for col in self.tasktable.columns:
			if col.name[:3]== "sch":
				info.append(col.name[4:])

		return info


	def dict(self):
		return {"prefix" : self.prefix, "name": self.name, "information" : self.information, "duration" : self.duration}


	def getInfo(self):
		self.setTables()
		data = self.dict()
		data["schemas"] = self.getMapInfo()
		
		data["originalnum"] = session.query(self.original).count()
		data["parsednum"] = session.query(self.parsed).count()
		data["tasknum"] = session.query(self.task).count()
		

		return data


	def getOriginals(self):
		return session.query(self.original).order_by(self.original.id).all()


	def getOriginal(self,id):
		return session.query(self.original).get(id)

	def checkUser(self,id):
		return self.enroll.filter(Enroll.userid == id).count() != 0

	def checkUserStatus(self,id):
		if self.checkUser(id):
			return self.enroll.filter(Enroll.userid == id).first().status
		else :
			return None


	def getParseds(self):
		return session.query(self.parsed).order_by(self.parsed.id).all()


	def getParsedBySubmitter(self,user):
		return session.query(self.parsed).filter(self.parsed.submitterid == user.id).order_by(self.parsed.id).all()

	def getParsedNumBySubmitter(self,user):
		return session.query(self.parsed).filter(self.parsed.submitterid == user.id).order_by(self.parsed.id).count()


	def addUser(self,user):
		enroll = Enroll()
		enroll.user = user
		self.enroll.append(enroll)
		session.commit()


	def getSubmitters(self):
		us = session.query(User,Enroll.status).join(User.enrolls).join(Enroll.task).filter(User.role == u"제출자").filter(Task.prefix == self.prefix).all()
		submitters = list()

		for user, status in us:
			u = user.dict()
			u["status"] = status
			submitters.append(u)

		return submitters

	def changeSubmitterStatus(self,userid,status):
		self.enroll.filter(Enroll.userid == userid).first().status = status
		session.commit()



	@staticmethod
	def checkPrefix(prefix):
		return session.query(Task).filter(Task.prefix == prefix).count() != 0


	@staticmethod
	def newTask(data):
		task = Task(data["name"],data["duration"],data["prefix"])
		task.information = data["information"]
		session.add(task)
		
		if task.generateTables(data["schemas"]):
			session.commit()
			
		return task

	@staticmethod
	def checkData(data):

		if len(data["schemas"]) == 0 :
			return u"스키마 정보가 없습니다."
		
		if not re.match("^[A-Za-z0-9_-]+$", data["prefix"]):
			return u"Prefix는영어,숫자, _ 문자열이야 합니다."
		try :
			int (data["duration"])
		except:
			return u"기간은 숫자이어야 합니다."

		if Task.checkPrefix(data["prefix"]):
			return u"이미 존재하는 Prefix입니다."


		for col in data["schemas"] :
			if not re.match("^[A-Za-z0-9_-]+$", col):
				return u"스키마는 영어,숫자, _ 문자열이야 합니다."


		return ""

	@staticmethod
	def checkOriginal(data):

		if len(data["schemas"]) == 0 :
			return u"스키마 정보가 없습니다."
		
		maplist = map(lambda x : x["col"],data["schemas"])


		if len(maplist) != len(set(maplist)):
			return u"매핑정보가 중복되었습니다."

		for mapinfo in maplist:
			if mapinfo >= data["length"]:
				return u"매핑정보가 길이보다 큽니다."
			try :
				int(mapinfo)
			except:
				return u"매핑정보는 숫자이어야 합니다."


		try :
			int (data["length"])
		except:
			return u"길이는 숫자이어야 합니다."

		if not Task.checkPrefix(data["prefix"]):
			return u"존재하지 않는 prefix입니다"





		return ""

	@staticmethod
	def getTasks(start=0,end=10):
		return session.query(Task).order_by(Task.prefix)[start:end]

	@staticmethod
	def getTask(prefix):
		task =  session.query(Task).filter(Task.prefix == prefix).first()
		if task :
			task.setTables()
		return task








