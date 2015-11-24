#-*- coding:utf-8 -*-
from DBP import app
#from flask_debugtoolbar import DebugToolbarExtension

if __name__ == '__main__':
#	toolbar = DebugToolbarExtension(app)
	app.run(host = '0.0.0.0', debug=True)