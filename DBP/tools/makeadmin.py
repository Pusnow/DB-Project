#-*- coding: utf-8 -*-


from DBP.models import Base,engine, session

from DBP.models.user import User


admin = User(u"admin",u"관리자",u"1234")
admin.role = u"관리자"
session.add(admin)
session.commit()