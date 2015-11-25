

from DBP.models import Base,engine, session
from sqlalchemy import  MetaData

from DBP.models.task import Task
from DBP.models.user import User, Enroll


Base.metadata.create_all(engine)

t = Task("test","TS")


d = ["data1","data2","data3"]

t.generateTables(d)
a =  t.original()
print dir(a)
t.setTables()
