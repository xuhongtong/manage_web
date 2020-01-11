from apps.auth.route import create_auth__register_blueprint
from apps.blog.route import create_blog__register_blueprint


# 注册全局蓝图
def create_register_blueprint(app):
    create_auth__register_blueprint(app)
    create_blog__register_blueprint(app)
