#-*- coding: utf-8 -*-

from DBP.models import Base,engine, session
from sqlalchemy import  MetaData
from datetime import datetime
from DBP.models.task import Task
from DBP.models.user import User, Enroll
import io


print User.login(u"admin", u"1234")








