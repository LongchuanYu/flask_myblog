# -*-coding:utf8 -*-
import os
import sqlite3,click
from flask import g,current_app
from flask.cli import with_appcontext

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session,sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:////test.db',convert_unicode=True)
db_session = scoped_session(sessionmaker(
	autocommit=False,
	autoflush=False,
	bind=engine
))
Base = declarative_base()
Base.query = db_session.query_property()


def init_db():
    import myapp.models
    #CREATE TABLE ...
    #创建models中所有的表
    Base.metadata.create_all(bind=engine)

@click.command('init-db')
@with_appcontext  
def init_db_command():
	init_db()
	click.echo('Initialized the database')

def init_app(app):
	#允许用户用命令行执行函数
	#比如 flask xxx
	app.cli.add_command(init_db_command)



# def get_db():
# 	if not 'db' in g:
# 		g.db = sqlite3.connect(
# 			os.path.join(current_app.instance_path,'myapp.sqlite'),
# 			detect_types=sqlite3.PARSE_DECLTYPES
# 		)
# 		g.db.row_factory = sqlite3.Row
# 	return g.db
# def close_db(e=None):
# 	if 'db' in g:
# 		db = g.pop('db')
# 		if db:
# 			db.close()



