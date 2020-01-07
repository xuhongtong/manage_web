import os

import redis

from flask_mail import Mail
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from config import mysql_info

db = SQLAlchemy()
mail = Mail()
sess = Session()

# 初始化数据库配置(SQLAlchemy)
def init_db(app):
    app.config[
        'SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{mysql_info["username"]}:{mysql_info["password"]}@{mysql_info["host"]}:{mysql_info["port"]}/{mysql_info["database"]}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    app.secret_key = '\xc9ixnRb\xe40\xd4\xa5\x7f\x03\xd0y6\x01\x1f\x96\xeao+\x8a\x9f\xe4'
    db.init_app(app)


# 初始化邮件配置(Mail)
def init_mail(app):
    app.config['MAIL_SERVER'] = 'smtp.163.com'
    app.config['MAIL_PORT'] = 465
    app.config['MAIL_USE_SSL'] = True
    app.config['MAIL_USE_TLS'] = False
    app.config['MAIL_USERNAME'] = 'xxx'
    app.config['MAIL_PASSWORD'] = 'xxx'
    mail.init_app(app=app)


# session 配置(Session)
def init_session(app):
    app.config['SESSION_TYPE'] = 'redis'  # session存储类型为redis
    app.config['SESSION_REDIS'] = redis.StrictRedis(host='192.168.199.129', port=6379, db=1)
    app.config['SESSION_USE_SIGNER'] = True  # 如果加盐，那么必须设置的安全码，盐
    app.config['SECRET_KEY'] = os.urandom(24)  # 如果加盐，那么必须设置的安全码，盐
    app.config['PERMANENT_SESSION_LIFETIME'] = 3600  # session长期有效，则设定session生命周期，整数秒，默认大概不到3小时。
    sess.init_app(app=app)
