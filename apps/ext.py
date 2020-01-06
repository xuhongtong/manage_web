from flask_login import LoginManager
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from itsdangerous import URLSafeTimedSerializer

from config import mysql_info

db = SQLAlchemy()
mail = Mail()


# 初始化数据库配置
def init_db(app):
    app.config[
        'SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{mysql_info["username"]}:{mysql_info["password"]}@{mysql_info["host"]}:{mysql_info["port"]}/{mysql_info["database"]}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    app.secret_key = '\xc9ixnRb\xe40\xd4\xa5\x7f\x03\xd0y6\x01\x1f\x96\xeao+\x8a\x9f\xe4'
    db.init_app(app)


# 初始化邮件配置
def init_mail(app):
    app.config['MAIL_SERVER'] = 'smtp.163.com'
    app.config['MAIL_PORT'] = 465
    app.config['MAIL_USE_SSL'] = True
    app.config['MAIL_USE_TLS'] = False
    app.config['MAIL_USERNAME'] = 'jingyetong@163.com'
    app.config['MAIL_PASSWORD'] = 'jinye123'
    mail.init_app(app=app)


# 初始化login
def init_login(app):
    login_manager = LoginManager()
    login_manager.session_protection = 'strong'
    login_manager.login_view = 'login'
    login_manager.init_app(app=app)


def generate_confirmation_token(email, app):
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    return serializer.dumps(email, salt=app.config['SECURITY_PASSWORD_SALT'])
