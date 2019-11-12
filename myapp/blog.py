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
        'SELECT p.id , title, SUBSTR(body,1,200) as body,created,author_id,username'
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


@bp.route('/article/<int:id>',methods=('GET','POST'))
def article(id):
    post = get_post(id,check_author=False)
    db=get_db()


    '''评论出现两条重复的原因在这里，这个JOIN之后会有重复，要考虑如何去重，还要考虑性能。。
    #评论的userid有问题，，JOIN这种操作还是运用不来
    'SELECT authorid,postid,userid,ctext,ctime,enable_dis,reply_targetid,u.username '
    ' FROM comment c JOIN user u ON c.authorid = ? and c.postid=?'
    ' WHERE u.id=c.authorid',
    (post['author_id'],post['id'])
    '''
    comments = db.execute(
        'SELECT authorid,postid,userid,ctext,ctime,enable_dis,reply_targetid,u.username '
        ' FROM comment c JOIN user u' 
        ' ON c.userid=u.id'
        ' WHERE c.authorid = ? and c.postid=?',
        (post['author_id'],post['id'])
    ).fetchall()
    # try:
    #     for com in comments:
    #         print(com['ctext'])
    # except:
    #     print("comment fetch error")
    
    if request.method=='POST':
        form_category = request.form['form_category']
        if form_category =="comment_send":
            comment_msg = request.form['comment_msg']
            #login_required必须
            if not g.user:
                return redirect(url_for('auth.login'))
            db = get_db()
            db.execute(
                'INSERT INTO comment'
                ' (authorid,postid,userid,ctext,enable_dis,reply_targetid)'
                ' VALUES'
                ' (?,?,?,?,?,?)',
                (post['author_id'],id,g.user['id'],comment_msg,True,-1)
            )
            db.commit()
            return redirect(url_for('blog.article',id=id))
        elif form_category =="comment_reply":
            pass
    return render_template('blog/article.html',post=post,comments=comments)

@bp.route('/article/reply/<int:postid>/<int:userid>')
def reply(postid,userid):
    print(postid,userid)
    return redirect(url_for('blog.article',id=postid))



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
    get_post(id)
    db = get_db()
    db.execute(
        'PRAGMA foreign_keys = ON'
    )
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
    if not post:
        abort(404,"Post None")
    if check_author and post['author_id']!=g.user['id']:
        abort(403)
    return post