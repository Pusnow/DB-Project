#-*- coding: utf-8 -*-

from sqlalchemy import create_engine
engine = create_engine('mysql+pymysql://root:root@localhost/dbproject?charset=utf8')
from sqlalchemy.orm import sessionmaker,scoped_session
session = scoped_session(sessionmaker(bind=engine))
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()