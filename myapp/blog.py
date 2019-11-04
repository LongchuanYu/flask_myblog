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
        # title = request.form['post_title']
        # body = request.form['post_text']
        title = request.form.get('post_title')
        body = request.form.get('ckeditor')
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


@bp.route('/article/<int:id>')
def article(id):
    post = get_post(id,check_author=False)
    return render_template('blog/article.html',post=post)



@bp.route('/update/<int:id>',methods=('GET','POST') )
@login_required
def update(id):
    post = get_post(id)
    if request.method=="POST":
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
                'UPDATE post SET title=?,body=?'
                ' WHERE id=?',
                (title,body,id)
            )
            db.commit()
            return redirect(url_for('blog.index'))
    return render_template('blog/create.html',post=post,update="True")

@bp.route('/delete/<int:id>')
@login_required
def delete(id):
    
    #易忘点：数据库查询要.fetchone()，不要忘了额
    # post = db.execute(
    #     'SELECT author_id'
    #     ' FROM post P'
    #     ' WHERE p.id=?',
    #     (id,)
    # ).fetchone()

    get_post(id)
    db = get_db()
    db.execute(
        'DELETE FROM post WHERE id=?',
        (id,)
    )
    #易忘点：数据库操作完毕都要commit一下
    db.commit()
    return redirect(url_for('blog.index'))



def get_post(id,check_author=True):
    db = get_db()
    post = db.execute(
        'SELECT p.id,title,body,created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' WHERE p.id=?' ,
        (id,)
    ).fetchone()
    if not post or not g.user:
        abort(404,"Post None")
    if check_author and post['author_id']!=g.user['id']:
        abort(403)
    return post