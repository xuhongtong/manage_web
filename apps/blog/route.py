# 注册认证蓝图
from apps.blog.views import blog


def create_blog__register_blueprint(app):
    app.register_blueprint(blog, prefix_url='/blog')
    app.register_blueprint(blog, prefix_url='/blogadmin')
    app.register_blueprint(blog, prefix_url='/info/<id>')
    app.register_blueprint(blog, prefix_url='/article')
    app.register_blueprint(blog, prefix_url='/category')
    app.register_blueprint(blog, prefix_url='/add_category')
    app.register_blueprint(blog, prefix_url='/add_article')
    app.register_blueprint(blog, prefix_url='/edit_article/<id>')
    app.register_blueprint(blog, prefix_url='/del_article/<id>')
    app.register_blueprint(blog, prefix_url='/edit_category/<id>')
    app.register_blueprint(blog, prefix_url='/del_category/<id>')

    # app.register_blueprint(blog, prefix_url='/edit_article')
    return app
