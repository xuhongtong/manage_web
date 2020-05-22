from flask import render_template, request, flash, session, redirect, url_for, abort
from flask import Blueprint

from apps.auth.models import User
from apps.auth.views import login_required
from apps.blog.models import Article, Category, Notice
from apps.ext import db, photos

blogadmin = Blueprint('blogadmin', __name__, template_folder='templates', static_folder='static')

@blogadmin.route('/article')
@login_required
def article():
    article_list = Article.query.filter(Article.is_delete == 0).all()
    user = User.query.filter(User.username == session.get('username')).first()
    content={
        'article_list':article_list,
        'user':user
    }
    return render_template('blogadmin/article_list.html', **content)


# 博客后台分类管理
@blogadmin.route('/category')
@login_required
def category():
    category_list = Category.query.filter(Category.is_delete == 0).all()
    user = User.query.filter(User.username == session.get('username')).first()
    content={
        'category_list':category_list,
        'user':user
    }
    return render_template('blogadmin/category_list.html', **content)


# 博客后台添加类别
@blogadmin.route('/add_category', methods=['GET', 'POST'])
@login_required
def add_category():
    if request.method == 'POST':
        category = Category(category=request.form.get('category'))
        db.session.add(category)
        db.session.commit()
        flash('分类添加成功')
    user = User.query.filter(User.username == session.get('username')).first()
    content={
        'user':user
    }
    return render_template('blogadmin/add_category.html',**content)


# 博客后台添加文章
@blogadmin.route('/add_article', methods=['GET', 'POST'])
@login_required
def add_article():
    if request.method == 'POST':
        c = Category.query.filter(Category.category == request.form.get('category')).first()
        u = User.query.filter(User.username == session.get('username')).first()
        article = Article(title=request.form.get('title'), tag1=request.form.get('tag1'), tag2=request.form.get('tag2'),
                          tag3=request.form.get('tag3'), content=request.form.get('content'),
                          short_content=request.form.get('short_content'),
                          category_id=c.id, author_id=u.id)
        db.create_all()
        db.session.add(article)
        db.session.commit()
        flash('文章发布成功')
    content = Category.query.filter(Category.is_delete == 0)
    user = User.query.filter(User.username == session.get('username')).first()
    content={
        'content':content,
        'user':user
    }
    return render_template('blogadmin/add_article.html', **content)


# 博客后台修改文章
@blogadmin.route('/edit_article/<id>', methods=['GET', 'POST'])
@login_required
def edit_article(id):
    if request.method == 'POST':
        u = Article.query.get(id)
        u.title = request.form.get('title')
        u.category_id = u.category.id
        u.tag1 = request.form.get('tag1')
        u.tag2 = request.form.get('tag2')
        u.tag3 = request.form.get('tag3')
        u.short_conent = request.form.get('short_conent')
        u.content = request.form.get('content')
        db.session.add(u)
        db.session.commit()
        flash('文章修改成功')
        return redirect(url_for('blog.info', id=id))
    article = Article.query.filter(Article.id == id).first()
    category_list = Category.query.all()
    user = User.query.filter(User.username == session.get('username')).first()
    content={
        'article':article,
        'category_list':category_list,
        'user':user
    }
    return render_template('blogadmin/edit_article.html', **content)


# 博客后台删除文章
@blogadmin.route('/del_article/<id>', methods=['GET', 'POST'])
@login_required
def del_article(id):
    u = Article.query.get(id)
    u.is_delete = 1
    db.session.add(u)
    db.session.commit()
    flash('文章删除成功')
    return redirect(url_for('blogadmin.article'))


# 博客后台修改类别
@blogadmin.route('/edit_category/<id>', methods=['GET', 'POST'])
@login_required
def edit_category(id):
    if request.method == 'POST':
        c = Category.query.get(id)
        c.category = request.form.get('category')
        db.session.add(c)
        db.session.commit()
        flash('类别修改成功')
        return redirect(url_for('blogadmin.category'))
    category = Category.query.filter(Category.id == id).first()
    user = User.query.filter(User.username == session.get('username')).first()
    content={
        'category':category,
        'user':user
    }
    return render_template('blogadmin/edit_category.html', **content)


# 博客后台删除类别
@blogadmin.route('/del_category/<id>', methods=['GET', 'POST'])
@login_required
def del_category(id):
    c = Category.query.get(id)
    c.is_delete = 1
    db.session.add(c)
    db.session.commit()
    flash('文章删除成功')
    return redirect(url_for('blogadmin.category'))


# 博客后台添加或编辑公告
@blogadmin.route('/edit_notice', methods=['GET', 'POST'])
@login_required
def edit_notice():
    if request.method == 'POST':
        db.create_all()
        n = Notice.query.filter(Notice.is_delete == 0).first()
        if not n:
            n = Notice(message=request.form.get('notice'), is_delete=0)
            db.session.add(n)
            db.session.commit()
            flash('公告添加成功')
            return redirect(url_for('blogadmin.home'))
        else:
            n.message = request.form.get('notice')
            db.session.add(n)
            db.session.commit()
            flash('公告修改成功')
            return redirect(url_for('blog.home'))
    user = User.query.filter(User.username == session.get('username')).first()
    content = {
        'user': user
    }
    return render_template('blogadmin/edit_notice.html',**content)


# 上传头像
@blogadmin.route('/upload', methods=['POST', 'GET'])
def upload():
    if request.method == 'POST':
        file_url = request.files.get('file')
        filename = photos.save(file_url)
        u = User.query.filter(User.username == session.get('username')).first()
        print(u.username)
        u.real_avator = filename
        db.session.add(u)
        db.session.commit()
        return redirect(url_for('blogadmin.article'))
    user = User.query.filter(User.username == session.get('username')).first()
    content = {
        'user': user
    }
    return render_template('blogadmin/upload.html',**content)


# 展示图片
@blogadmin.route('/photo/<name>')
def show(name):
    if name is None:
        abort(404)
    url = photos.url(name)
    return render_template('show.html', url=url, name=name)
