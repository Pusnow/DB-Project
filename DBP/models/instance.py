#-*- coding: utf-8 -*-


from DBP.models import Base, session
from DBP.models.user import randomEvaluator
from sqlalchemy.orm import class_mapper
from sqlalchemy.inspection import inspect
import csv
import io


class OriginalData (object):

	


	def __init__(self, length, name, mappinginfo):
		self.length = length
		self.name  = name
		cols = inspect(self.__class__).columns
		if len(mappinginfo) != len(cols) -3:
			raise TypeError

		for col in cols:

			if not col.name[:3] == u"sch":
				continue


			if int(mappinginfo[col.name]) >= self.length :
				raise TypeError
			setattr(self,col.name,int(mappinginfo[col.name]))


	def mapList(self):
		maplist = list()
		for col in inspect(self.__class__).columns:
			if not col.name[:3] == u"sch":
				continue


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
				crow.append(unicode(rrow[mapnum]))

			writer.writerow(crow)
			counter += 1


		evaluator = randomEvaluator()
		
		parsedmodel =  self.parsedclass(nth,duration_start,duration_end,csvwrite,counter, counter - len(dupset))
		parsedmodel.submitter = submitter.id
		parsedmodel.evaluator = evaluator.id
		self.parsed.append(parsedmodel)

		session.commit()



class ParsedData (object):

	def __init__(self,nth,duration_start,duration_end, csvfile, tuplenum,duplicatetuplenum):
		self.nth = nth
		self.duration_start = duration_start
		self.duration_end = duration_end
		self.file = csvfile.getvalue()
		self.tuplenum = tuplenum
		self.duplicatetuplenum = duplicatetuplenum




class TaskData (object):
	pass


