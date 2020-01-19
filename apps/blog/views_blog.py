import math

from flask import render_template, request, flash, redirect, url_for
from flask import Blueprint
from flask_paginate import get_page_parameter, Pagination

from apps.blog.models import Article, Category, Notice, Comment
from apps.ext import db

blog = Blueprint('blog', __name__, template_folder='templates', static_folder='static')


# 首页
@blog.route('/blog')
def home():
    per_page=3
    total=Article.query.count()
    page=request.args.get(get_page_parameter(),type=int,default=1)
    start=(page-1)*per_page
    end=start+per_page
    pagination=Pagination(bs_version=3,page=page,total=total)
    pagination.per_page=3
    pagination.numpages=math.ceil(pagination.total/pagination.per_page)
    pagination.page_list = []
    for i in range(0,pagination.numpages):
        pagination.page_list.append(i+1)
    pagination.has_next= True if pagination.page<pagination.numpages else False
    pagination.before_page=pagination.page-1
    pagination.after_page=pagination.page+1
    articles=Article.query.filter(Article.is_delete == 0).slice(start,end)
    notice = Notice.query.filter(Notice.is_delete == 0).first()
    category_list = Category.query.filter(Category.is_delete == 0)
    content = {
        'content': articles,
        'notice': notice,
        'category_list': category_list,
        'pagination': pagination,
    }
    return render_template('blog/index.html', **content)


# 分类页
@blog.route('/filter_category/<id>')
def filter_category(id):
    content_list = Article.query.filter(Article.category_id == id, Article.is_delete == 0)
    notice = Notice.query.filter(Notice.is_delete == 0).first()
    category_list = Category.query.filter(Category.is_delete == 0)
    content = {
        'content_list': content_list,
        'notice': notice,
        'category_list': category_list
    }
    return render_template('blog/category.html', **content)


# 详情页
@blog.route('/info/<id>')
def info(id):
    article = Article.query.filter(Article.id == id).first()
    notice = Notice.query.filter(Notice.is_delete == 0).first(),
    category_list = Category.query.filter(Category.is_delete == 0)
    comment_list=Comment.query.all()
    content = {
        'article': article,
        'notice': notice,
        'category_list': category_list,
        'comment_list':comment_list
    }
    return render_template('blog/info.html', **content)


# 文章搜索
@blog.route('/search', methods=['GET', 'POST'])
def w_search():
    if request.method == 'POST':
        keyword = request.form.get('keyboard')
        results = Article.query.filter(Article.is_delete == 0).msearch(keyword, fields=['title'], limit=20)
        notice = Notice.query.filter(Notice.is_delete == 0).first()
        content = {
            'results': results,
            'notice': notice
        }
        return render_template('blog/search.html', **content)

# 添加评论
@blog.route('/comment/<id>', methods=['GET', 'POST'])
def add_comment(id):
    if request.method == 'POST':
        db.create_all()
        content=request.form.get('content')
        username=request.form.get('username')
        c=Comment(content=content,nickname=username)
        db.session.add(c)
        db.session.commit()
        flash('添加评论成功')
        return redirect(url_for('blog.info',id=id))