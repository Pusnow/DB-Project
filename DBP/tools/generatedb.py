#-*- coding: utf-8 -*-

from DBP.models import Base, engine
from DBP.models.task import Task
from DBP.models.user import User, Enroll

Base.metadata.create_all(engine) 