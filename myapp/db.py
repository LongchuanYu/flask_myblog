# -*-coding:utf8 -*-
import os
import sqlite3,click
from flask import g,current_app
from flask.cli import with_appcontext
def get_db():
	if not 'db' in g:
		g.db = sqlite3.connect(
			os.path.join(current_app.instance_path,'myapp.sqlite'),
			detect_types=sqlite3.PARSE_DECLTYPES
		)
		g.db.row_factory = sqlite3.Row
	return g.db
def close_db(e=None):
	if 'db' in g:
		db = g.pop('db')
		if db:
			db.close()


def init_db():
	db = get_db()
	with current_app.open_resource('schema.sql') as f:
		db.executescript(f.read().decode('utf8'))

@click.command('init-db')
@with_appcontext  
def init_db_command():
	init_db()
	click.echo('Initialized the database')

def init_app(app):
	app.teardown_appcontext(close_db)
	#允许用户用命令行执行函数
	#比如 flask xxx
	app.cli.add_command(init_db_command)