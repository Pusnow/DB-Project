#-*- coding: utf-8 -*-


from DBP.models import Base



class OriginalData (object):

	__table_args__  = {'autoload':True}
	def test(self):
		print self.__table__
	pass



class TaskData (object):
	pass


class ParsedData (object):
	pass