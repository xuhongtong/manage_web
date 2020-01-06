from flask import Flask
from apps.auth.route import create_register_blueprint
from apps.ext import init_db, init_mail


def create_app():
    app = Flask(__name__)     # 初始化flask（全局）
    init_db(app)              # 初始化数据库(全局）
    init_mail(app)            # 初始化邮件配置（全局）
    create_register_blueprint(app)      # 注册蓝图（全局）
    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
