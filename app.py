from flask import Flask
from apps.all_blueprint import create_register_blueprint
from apps.ext import init_db, init_mail, init_session, init_ckeditor, init_WhooshAlchemy, init_uploads


# from apps.fk_admin import init_admin


def create_app():
    app = Flask(__name__)  # 初始化flask（全局）
    init_db(app)  # 初始化数据库(全局）
    init_mail(app)  # 初始化邮件配置（全局）
    init_session(app)  # 初始化session配置
    init_ckeditor(app)
    init_WhooshAlchemy(app)
    init_uploads(app)
    # init_admin(app)
    create_register_blueprint(app)  # 注册蓝图（全局）
    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
