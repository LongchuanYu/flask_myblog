# -*-coding:utf8 -*-
from flask import (
    Blueprint,flash,g,redirect,render_template,request,url_for
)
from myapp.auth import login_required
from myapp.db import get_db
from werkzeug.exceptions import abort

bp=Blueprint('blog',__name__)

@bp.route('/')
def index():
    db = get_db()
    posts = db.execute(
        'SELECT p.id , title, SUBSTR(body,1,100) as body,created,author_id,username'
        '  FROM post p JOIN user u ON p.author_id = u.id'
        '  ORDER BY created DESC'
    ).fetchall()

    return render_template('blog/index.html',posts=posts)

#新增文章之前需要验证用户是否处于登录状态
@bp.route('/create',methods=('GET','POST'))
@login_required
def create():
    if request.method=='POST':
        title = request.form['post_title']
        body = request.form['post_text']
        error=None
        if not title:
            error = 'Title is required'
        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO post (title,body,author_id) VALUES (?,?,?)',
                (title,body,g.user['id'])
            )
            db.commit()
            return redirect(url_for('blog.index'))
    return render_template('blog/create.html')
@bp.route('article/<int:id>')
@login_required
def article(id):
    db = get_db()
    post = db.execute(
        'SELECT p.id,title,body,created, author_id, username'
        'FROM post p JOIN user u ON p.author_id = u.id'
        'WHERE p.id=?',
        (id,)
    ).fetchone()
    if not post:
        abort(404,'Post is None')
    else:
        return render_template('blog/article.html')







