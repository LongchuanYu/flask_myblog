# -*-coding:utf8 -*-
#顶头加一句编码集，不然注释会报错
import os
from flask import Flask,g
from flask_ckeditor import CKEditor

ckeditor = CKEditor()
def create_app():
	app = Flask(__name__)
	

	#一定要添加SECRET_KEY啊，不然post请求会报错no secret key was set
	app.config['SECRET_KEY']='dev' 
	app.DEBUG=True
	app.config['CKEDITOR_SERVE_LOCAL'] = True
	app.config['CKEDITOR_HEIGHT'] = 400
	try:
		os.makedirs(app.instance_path)
	except OSError:
		print('makedirs existed')

	@app.template_filter('ellipsis')
	def do_ellipsis(arg):
		import re
		return re.sub(r"<.*?>",'',arg)



	from . import db
	db.init_app(app)
	from . import auth
	app.register_blueprint(auth.bp)

	from . import blog
	app.register_blueprint(blog.bp)
	app.add_url_rule('/',endpoint='index')

	
	ckeditor.init_app(app)
	return app