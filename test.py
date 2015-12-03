#-*- coding: utf-8 -*-

from DBP.models import Base,engine, session
from sqlalchemy import  MetaData
from datetime import datetime
from DBP.models.task import Task
from DBP.models.user import User, Enroll
import io

Base.metadata.create_all(engine)
str(datetime.now())
evaluator = User(u"evaluator" + str(datetime.now()),u"김똘똘",u"1234")
evaluator.role = u"평가자"

submitter = User(u"submitter" + str(datetime.now()),u"김똘똘2",u"1234")


session.add(evaluator)
session.add(submitter)

session.commit()



t = Task("test",datetime.now(),"TS")

d = ["data1","data2","data3"]

t.generateTables(d)
mapinfo = {
	"sch_data1" : 3 ,
	"sch_data2" : 1 ,
	"sch_data3" : 5}
name = u"하나카드"
length = 6
t.setTables()
om = t.newOriginal(length,name,mapinfo)


csvdata = u"""'1','45','32','23','21','312'
'1','45','32','23','21','312'
'1','45','32','23','21','312'
'1','45','32','23','21','312'
'1','45','32','23','21','312'
"""
csvtest = io.StringIO(csvdata)
pd = om.loadcsv(submitter,csvtest,1,datetime(2015, 1, 1),datetime(2016, 1, 1))

pd.pnp = "Pass"

print User.login(evaluator.loginid, u"1234h")








