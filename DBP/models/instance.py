#-*- coding: utf-8 -*-


from DBP.models import Base, session
from DBP.models.user import User
from sqlalchemy.orm import class_mapper
from sqlalchemy.inspection import inspect
from sqlalchemy.sql import func
import csv
import io


class OriginalData (object):

	


	def __init__(self, length, name, mappinginfo):
		self.length = length
		self.name  = name
		cols = inspect(self.__class__).columns
		if len(mappinginfo) != len(cols) -3:
			raise TypeError

		for col in mappinginfo:
			setattr(self,str( u"sch_"+col["label"]),int(col["col"]))


	def dict(self):
		data = {
			"id" : self.id,
			"length" : self.length,
			"name" : self.name,
			"mapinfo" : self.mapList()
		}
		return data

	def mapList(self):
		maplist = list()
		for col in filter(lambda x: x.name[:3] == u"sch", inspect(self.__class__).columns ):
			maplist.append(getattr(self,col.name))
		return maplist


	def loadcsv(self,submitter,csvread,nth,duration_start,duration_end):
		reader = csv.reader(csvread, delimiter=',', quotechar="'")
		csvwrite = io.BytesIO()
		writer =  csv.writer(csvwrite, delimiter=',', quotechar="'")
		maplist = self.mapList()
		counter = 0
		dupset = set()
		dupcounter = 0
		for rrow in reader:
			crow = list()
			dupset.add(unicode(rrow))
			for mapnum in maplist:
				crow.append(rrow[mapnum])

			writer.writerow(crow)
			counter += 1


		evaluator = User.randomEvaluator()
		
		parsedmodel =  self.parsedclass(nth,duration_start,duration_end,csvwrite,counter, counter - len(dupset))
		parsedmodel.submitterid = submitter.id
		parsedmodel.evaluatorid = evaluator.id
		self.parseds.append(parsedmodel)

		session.commit()

		return parsedmodel

	def getInfoByUser(self,user):
		data = self.dict()
		nth =  session.query( func.max(self.parsedclass.nth)).filter(self.parsedclass.submitterid == user.id).first()
		
		data["nth"] = self.getNextnth (user)


		return data


	def getNextnth(self,user):
		nth =  session.query( func.max(self.parsedclass.nth)).filter(self.parsedclass.submitterid == user.id).first()
		if nth[0]:
			return nth[0] +1
		else :
			return 1

	



class ParsedData (object):

	def __init__(self,nth,duration_start,duration_end, csvfile, tuplenum,duplicatetuplenum):
		self.nth = nth
		self.duration_start = duration_start
		self.duration_end = duration_end
		self.file = csvfile.getvalue()
		self.tuplenum = tuplenum
		self.duplicatetuplenum = duplicatetuplenum


	def parsecsv(self):
		csvread = io.StringIO(unicode(self.file))
		reader = csv.reader(csvread, delimiter=',', quotechar="'")
		parsedlist = list()
		for row in reader:
			tsmodel = self.taskclass(User.getUser(self.submitterid).name, self.id)
			for (column, data) in zip(filter(lambda x: x.name[:3] == u"sch", inspect(self.taskclass).columns ), row):
				setattr(tsmodel,column.name, data)

			parsedlist.append(tsmodel)

		return parsedlist


	def insertcsv(self):
		if self.pnp != "Pass":
			return False

		session.bulk_save_objects(self.parsecsv())
		session.commit()
		return True


	def dict(self):

		return {
			"nth" : self.nth,
			"tuplenum" : self.tuplenum,
			"duplicatetuplenum" : self.duplicatetuplenum,
			"duration_start" : self.duration_start.isoformat(),
			"duration_end" : self.duration_end.isoformat(),
			"status" : self.status,
			"score" : self.score,
			"pnp" : self.pnp,
			"submitter" : User.getUser(self.submitterid).name,
			"original" : self.original.name

		}








class TaskData (object):
	
	def __init__ (self,submittername, parsedid):
		self.submittername = submittername
		self.parsedid = parsedid


