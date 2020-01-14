from flask import render_template, request
from flask import Blueprint
from apps.blog.models import Article, Category, Notice

blog = Blueprint('blog', __name__, template_folder='templates', static_folder='static')


# 首页
@blog.route('/blog')
def home():
    content = Article.query.filter(Article.is_delete == 0)
    notice = Notice.query.filter(Notice.is_delete == 0).first()
    category_list = Category.query.filter(Category.is_delete == 0)
    content = {
        'content': content,
        'notice': notice,
        'category_list': category_list
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
    content = {
        'article': article,
        'notice': notice,
        'category_list': category_list
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
