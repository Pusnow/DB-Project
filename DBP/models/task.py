#-*- coding: utf-8 -*-

from DBP.models import Base, engine, session
from sqlalchemy import Column,  Unicode, Text, DateTime, Integer, BLOB, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy import Table, MetaData
from DBP.models.instance import OriginalData, TaskData, ParsedData
from sqlalchemy.orm import mapper
from DBP.models.user import User




class Task(Base):
	__tablename__ = 'Task'
	name = Column(Unicode(100),primary_key = True)
	information = Column(Text)
	duration = Column(DateTime, nullable = False)
	prefix = Column(Unicode(10), unique = True, nullable = False)


	def __init__(self,name,prefix):
		self.name = name[:100]
		self.prefix = prefix[:10]



	def setTables(self):
		metadata = Base.metadata
		originalTableName = self.prefix + "_OriginalData"
		parsedTableName = self.prefix + "_ParsedData"
		taskTableName = self.prefix + "_TaskData"
		self.originaltable = Table(originalTableName, metadata, autoload=True, autoload_with=engine)
		self.parsedtable = Table(parsedTableName, metadata, autoload=True, autoload_with=engine)
		self.tasktable = Table(taskTableName, metadata, autoload=True, autoload_with=engine)

		self.original = type(originalTableName,(OriginalData,),{})
		self.parsed = type(parsedTableName,(ParsedData,),{})
		self.task = type(taskTableName,(TaskData,),{})
		mapper(self.original, self.originaltable, properties={
			'parsed': relationship(self.parsed, backref='original')
		})
		mapper(self.parsed, self.parsedtable, properties={
			'task': relationship(self.task, backref='parsed')
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
			Column('evaluator', Integer, ForeignKey('User.id'), nullable = False),
			Column('status',Enum('Waiting','Evaluated'), nullable = False, server_default = 'Waiting'),
			Column('score',Integer, nullable = False, server_default= "0"),
			Column('pnp',Enum('Pass','Nonpass'), nullable = False, server_default = 'Nonpass'),
			Column('submitter', Integer, ForeignKey('User.id'), nullable = False)
			#,autoload=True, autoload_with=engine
			)


		#task data
		
		taskTableName = self.prefix + "_TaskData"
		self.tasktable = Table(taskTableName,metadata,
			Column('id', Integer, primary_key=True,autoincrement = True),
			Column('submittername', Unicode(100), nullable = False),
			Column('parsedid', Integer, ForeignKey(parsedTableName+'.id'), nullable = False),
			*(Column("sch_"+colname, Integer) for colname in mappinginfo)
			#,autoload=True, autoload_with=engine
			)

		metadata.create_all(bind= engine)


		self.original = type(originalTableName,(OriginalData,),{})
		self.parsed = type(parsedTableName,(ParsedData,),{})
		self.task = type(taskTableName,(TaskData,),{})
		mapper(self.original, self.originaltable)
		mapper(self.parsed, self.parsedtable, properties={
			'original': relationship(self.original, backref='parsed')
		})
		mapper(self.task, self.tasktable, properties={
			'parsed': relationship(self.parsed, backref='task')
		})

		self.original.parsedclass = self.parsed
		self.parsed.taskclass = self.task





	def newOriginal(self, length, name,mappinginfo):
		originalmodel = self.original(length, name,mappinginfo)
		session.add(originalmodel)
		session.commit()
		return originalmodel



	def getMapInfo(self):
		info = list()
		for col in self.tasktable.columns:
			if col.name[:3]== "sch":
				info.append({"name" : col.name, "type" : col.type })

		return info
		
		










