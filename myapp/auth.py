# -*-coding:utf8 -*-
import functools
from flask import(
    Blueprint,flash,g,redirect,render_template,request,session,url_for
)
from db import get_db
from werkzeug.security import generate_password_hash,check_password_hash
bp = Blueprint('auth',__name__,url_prefix='/auth')

@bp.route('/register',methods=('GET','POST'))
def register():
	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']
		db=get_db()
		error=None
		if not username:
			error = 'username error'
		elif not password:
			error = 'password error'
		elif db.execute(
			'SELECT id FROM user WHERE username=?',(username,)
		).fetchone() is not None:
			error = '{} is already existed'.format(username)
		
		if error is None:

			db.execute(
				'INSERT INTO user (username,password) VALUES (?,?)',
				(username,generate_password_hash(password))
			)
			db.commit()
			#注册成功后重定向的页面
			return redirect('http://www.baidu.com')
		flash(error)
	return render_template('auth/register.html')
			
@bp.route('/login',methods=('GET','POST'))
def login():
	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']
		db = get_db()
		error = None
		dbuser = db.execute(
			'SELECT * FROM user WHERE username=?',(username,)
		).fetchone()
		if dbuser is None:
			error = 'Incorrect username'
		elif not check_password_hash(dbuser['password'],password):
			error = 'Incorrect password'
		if error is None:
			session.clear()
			session['user_id'] = dbuser['id']

			#疑问：这里是怎么找到index的？
			#作为蓝图是继承了db.py,因此能找到db.py里面的函数
			#db.py中用add_url_rule('/',endpoint='index')来关联端点名称
			return redirect(url_for('index'))
	return render_template('auth/login.html')

@bp.route('/logout')
def logout():
	session.clear()
	return redirect(url_for('auth.login'))


#before_app_request会在任何请求之前运行
#无论该装饰器写在哪个文件中
@bp.before_app_request
def load_logged_in_user():
	'''之后可以从g.user判断用户是否处于登录状态
	session有值证明用户已登录，从db获取用户id存到g.user
	没有值则设置g.user=None
	'''
	user_id = session.get('user_id')
	if user_id is None:
		g.user = None
	else:
		g.user = get_db().execute(
			'SELECT * FROM user WHERE id=?',(user_id,)
		).fetchone()

def login_required(view):
	#此处如果不加@functools.wraps(view)
	#会造成在base.html中url_for('blog.create') 报错
	#	应该是blog.py中的create函数经过包装
	#	导致flask已经找不到create这个函数了
	#	而@functools.wraps(view)的功能就是保留原函数的特性
	@functools.wraps(view)
	def wrapped_view(**kwargs):
		if g.user is None: #用户未登录
			return redirect(url_for('auth.login'))
		return view(**kwargs)
	return wrapped_view