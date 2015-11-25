#-*- coding: utf-8 -*-


from DBP.models import Base, engine
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
		original = Table(originalTableName, metadata, autoload=True, autoload_with=engine)
		parsed = Table(parsedTableName, metadata, autoload=True, autoload_with=engine)
		task = Table(taskTableName, metadata, autoload=True, autoload_with=engine)

		self.original = type(originalTableName,(OriginalData,),{})
		self.parsed = type(parsedTableName,(ParsedData,),{})
		self.task = type(taskTableName,(TaskData,),{})
		mapper(self.original, original)
		mapper(self.parsed, parsed)
		mapper(self.task, task)



	def generateTables(self,mappinginfo):
		metadata = Base.metadata
		#original data

		originalTableName = self.prefix + "_OriginalData"
		
		original = Table(originalTableName,metadata,
			Column('id', Integer, primary_key=True),
			*(Column("sch_"+colname, Integer) for colname in mappinginfo)
			,autoload=True, autoload_with=engine
			)


		#parsed data
		parsedTableName = self.prefix + "_ParsedData"

		parsed = Table(parsedTableName,metadata,
			Column('id', Integer, primary_key=True),
			Column('duration', DateTime, nullable = False),
			Column('count', Integer, nullable = False, server_default = "0"),
			Column('file',BLOB, nullable = False),
			Column('tuplenum',Integer, nullable = False),
			Column('duplicatetuplenum',Integer, nullable = False),
			Column('originalid', Integer, ForeignKey(originalTableName+'.id'), nullable = False),
			Column('evaluator', Unicode(30), ForeignKey('User.id'), nullable = False),
			Column('status',Enum('Waiting','Evaluated'), nullable = False, server_default = 'Waiting'),
			Column('score',Integer, nullable = False, server_default= "0"),
			Column('pnp',Enum('Pass','Nonpass'), nullable = False, server_default = 'Nonpass'),
			Column('submitter', Unicode(30), ForeignKey('User.id'), nullable = False)
			,autoload=True, autoload_with=engine
			)


		#task data
		
		taskTableName = self.prefix + "_TaskData"
		task = Table(taskTableName,metadata,
			Column('id', Integer, primary_key=True),
			Column('submittername', Unicode(100), nullable = False),
			Column('parsedid', Integer, ForeignKey(parsedTableName+'.id'), nullable = False),
			*(Column("sch_"+colname, Integer) for colname in mappinginfo)
			,autoload=True, autoload_with=engine
			)

		metadata.create_all(bind= engine)


		self.original = type(originalTableName,(OriginalData,),{})
		self.parsed = type(parsedTableName,(ParsedData,),{})
		self.task = type(taskTableName,(TaskData,),{})
		mapper(self.original, original)
		mapper(self.parsed, parsed)
		mapper(self.task, task)




	def newOriginal(self,mappinginfo):
		pass
		










