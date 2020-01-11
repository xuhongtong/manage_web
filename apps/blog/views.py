from flask import render_template, request, flash, session, redirect, url_for
from flask import Blueprint

from apps.auth.models import User
from apps.auth.views import login_required
from apps.blog.models import Article, Category, Notice
from apps.ext import db

blog = Blueprint('blog', __name__, template_folder='templates', static_folder='static')


# 博客展示页面

# 首页
@blog.route('/blog')
def home():
    return render_template('blog/index.html', content=Article.query.all(),
                           notice=Notice.query.filter(Notice.is_delete == 0).first(),
                           category_list=Category.query.filter(Category.is_delete == 0))


# 分类页
@blog.route('/filter_category/<id>')
def filter_category(id):
    return render_template('blog/category.html', content_list=Article.query.filter(Article.category_id == id),
                           notice=Notice.query.filter(Notice.is_delete == 0).first(),
                           category_list=Category.query.filter(Category.is_delete == 0))


# 详情页
@blog.route('/info/<id>')
def info(id):
    article = Article.query.filter(Article.id == id).first()
    return render_template('blog/info.html', article=article, notice=Notice.query.filter(Notice.is_delete == 0).first(),
                           category_list=Category.query.filter(Category.is_delete == 0))

# 博客后台
# 博客后台文章管理
@blog.route('/article')
@login_required
def article():
    article_list = Article.query.filter(Article.is_delete == 0).all()
    return render_template('blogadmin/article_list.html', article_list=article_list)

# 博客后台分类管理
@blog.route('/category')
@login_required
def category():
    category_list = Category.query.filter(Category.is_delete == 0).all()
    return render_template('blogadmin/category_list.html', category_list=category_list)

# 博客后台添加类别
@blog.route('/add_category', methods=['GET', 'POST'])
@login_required
def add_category():
    if request.method == 'POST':
        category = Category(category=request.form.get('category'))
        db.session.add(category)
        db.session.commit()
        flash('分类添加成功')
    return render_template('blogadmin/add_category.html')

# 博客后台添加文章
@blog.route('/add_article', methods=['GET', 'POST'])
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
    return render_template('blogadmin/add_article.html', content=Category.query.filter(Category.is_delete == 0))

# 博客后台修改文章
@blog.route('/edit_article/<id>', methods=['GET', 'POST'])
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
    print(article.category.category)
    print(article.short_content)
    category_list = Category.query.all()
    return render_template('blogadmin/edit_article.html', article=article, category_list=category_list)

# 博客后台删除文章
@blog.route('/del_article/<id>', methods=['GET', 'POST'])
@login_required
def del_article(id):
    u = Article.query.get(id)
    u.is_delete = 1
    db.session.add(u)
    db.session.commit()
    flash('文章删除成功')
    return redirect(url_for('blog.article'))

# 博客后台修改类别
@blog.route('/edit_category/<id>', methods=['GET', 'POST'])
@login_required
def edit_category(id):
    if request.method == 'POST':
        c = Category.query.get(id)
        c.category = request.form.get('category')
        db.session.add(c)
        db.session.commit()
        flash('类别修改成功')
        return redirect(url_for('blog.category'))
    category = Category.query.filter(Category.id == id).first()
    return render_template('blogadmin/edit_category.html', category=category)

# 博客后台删除类别
@blog.route('/del_category/<id>', methods=['GET', 'POST'])
@login_required
def del_category(id):
    c = Category.query.get(id)
    c.is_delete = 1
    db.session.add(c)
    db.session.commit()
    flash('文章删除成功')
    return redirect(url_for('blog.category'))

# 博客后台添加或编辑公告
@blog.route('/edit_notice', methods=['GET', 'POST'])
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
            return redirect(url_for('blog.home'))
        else:
            n.message = request.form.get('notice')
            db.session.add(n)
            db.session.commit()
            flash('公告修改成功')
            return redirect(url_for('blog.home'))
    return render_template('blogadmin/edit_notice.html')
