# 注册认证蓝图
from apps.blog.views_blog import blog
from apps.blog.views_blogadmin import blogadmin


def create_blog__register_blueprint(app):
    app.register_blueprint(blog, prefix_url='/blog')    # 博客展示首页
    app.register_blueprint(blog, prefix_url='/filter_category/<id>')  
    app.register_blueprint(blog, prefix_url='/info/<id>')   # 博客文章详情页面
    app.register_blueprint(blog, prefix_url='/search')  # 博客文章搜索结果页面
    app.register_blueprint(blogadmin, prefix_url='/article')    # 博客后台文章列表
    app.register_blueprint(blogadmin, prefix_url='/category')   # 博客后台分类列表
    app.register_blueprint(blogadmin, prefix_url='/add_category')  # 博客后台添加分类
    app.register_blueprint(blogadmin, prefix_url='/add_article')   # 博客后台添加文章
    app.register_blueprint(blogadmin, prefix_url='/edit_article/<id>') # 博客后台编辑文章
    app.register_blueprint(blogadmin, prefix_url='/del_article/<id>')  # 博客后台删除文章
    app.register_blueprint(blogadmin, prefix_url='/edit_category/<id>')  # 博客后台编辑分类
    app.register_blueprint(blogadmin, prefix_url='/del_category/<id>')  # 博客后台删除分类
    app.register_blueprint(blogadmin, prefix_url='/edit_notice')      # 博客后台编辑公告
    app.register_blueprint(blogadmin, prefix_url='/upload')    # 博客后台上传头像
    return app
