# 注册认证蓝图
from apps.blog.views_blog import blog
from apps.blog.views_blogadmin import blogadmin


def create_blog__register_blueprint(app):
    app.register_blueprint(blog, prefix_url='/blog')
    app.register_blueprint(blog, prefix_url='/filter_category/<id>')
    app.register_blueprint(blog, prefix_url='/info/<id>')
    app.register_blueprint(blog, prefix_url='/search')
    app.register_blueprint(blogadmin, prefix_url='/article')
    app.register_blueprint(blogadmin, prefix_url='/category')
    app.register_blueprint(blogadmin, prefix_url='/add_category')
    app.register_blueprint(blogadmin, prefix_url='/add_article')
    app.register_blueprint(blogadmin, prefix_url='/edit_article/<id>')
    app.register_blueprint(blogadmin, prefix_url='/del_article/<id>')
    app.register_blueprint(blogadmin, prefix_url='/edit_category/<id>')
    app.register_blueprint(blogadmin, prefix_url='/del_category/<id>')
    app.register_blueprint(blogadmin, prefix_url='/edit_notice')
    app.register_blueprint(blogadmin, prefix_url='/upload')
    return app
