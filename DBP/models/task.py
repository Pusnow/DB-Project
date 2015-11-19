#-*- coding: utf-8 -*-


from DBP.models import Base, engine
from sqlalchemy import Column,  Unicode, Text, DateTime, Integer, BLOB, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy import Table, MetaData
from DBP.models.instance import OriginalData, TaskData, ParsedData

from DBP.models.user import User




class Task(Base):
	__tablename__ = 'Task'
	name = Column(Unicode(100),primary_key = True)
	information = Column(Text)
	duration = Column(DateTime)
	prefix = Column(Unicode(10), unique = True)


	def __init__(self,name,prefix):
		self.name = name[:100]
		self.prefix = prefix[:10]



	def generateTables(self,mappinginfo):
		metadata = Base.metadata
		#original data

		originalTableName = self.prefix + "_OriginalData"
		
		original = Table(originalTableName,metadata,
			Column('id', Integer, primary_key=True),
			*(Column(colname, Integer) for colname in mappinginfo)
			)


		#parsed data
		parsedTableName = self.prefix + "_ParsedData"

		parsed = Table(parsedTableName,metadata,
			Column('id', Integer, primary_key=True),
			Column('duration', DateTime),
			Column('count', Integer),
			Column('file',BLOB),
			Column('tuplenum',Integer),
			Column('duplicatetuplenum',Integer),
			Column('originalid', Integer, ForeignKey(originalTableName+'.id')),
			Column('evaluator', Integer, ForeignKey('User.id')),
			Column('status',Enum('Waiting','Evaluated')),
			Column('score',Integer),
			Column('pnp',Enum('Pass','Nonpass')),
			Column('submitter', Integer, ForeignKey('User.id'))

			)


		#task data
		
		taskTableName = self.prefix + "_TaskData"
		parsed = Table(taskTableName,metadata,
			Column('id', Integer, primary_key=True),
			Column('submittername', Unicode(100)),
			Column('parsedid', Integer, ForeignKey(parsedTableName+'.id')),
			*(Column(colname, Integer) for colname in mappinginfo)
			)

		metadata.create_all(bind= engine)