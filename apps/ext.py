import redis
from flask_ckeditor import CKEditor
from flask_mail import Mail
from flask_msearch import Search
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from flask_uploads import IMAGES, UploadSet, configure_uploads
from whoosh.analysis import StemmingAnalyzer

from config import mysql_info, WHOOSH_BASE, MAIL_USERNAME, MAIL_PASSWORD

db = SQLAlchemy()
mail = Mail()
sess = Session()
ckeditor = CKEditor()
search = Search()
photos = UploadSet('image')


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
    app.config['MAIL_USERNAME'] = MAIL_USERNAME
    app.config['MAIL_PASSWORD'] = MAIL_PASSWORD
    mail.init_app(app=app)


# 初始化FlaskElasticsearch
def init_WhooshAlchemy(app):
    app.config['WHOOSH_BASE'] = WHOOSH_BASE
    app.config['WHOOSH_ANALYZER'] = StemmingAnalyzer()
    search.init_app(app)


# session 配置(Session)
def init_session(app):
    app.config['SESSION_TYPE'] = 'redis'  # session存储类型为redis
    app.config['SESSION_REDIS'] = redis.StrictRedis(host='192.168.199.129', port=6379, db=1)
    app.config['SESSION_USE_SIGNER'] = True  # 如果加盐，那么必须设置的安全码，盐
    app.config['SECRET_KEY'] = 'asfsdfffdfgdfsdfdfgggggdg'  # 如果加盐，那么必须设置的安全码，盐
    app.config['PERMANENT_SESSION_LIFETIME'] = 3600  # session长期有效，则设定session生命周期，整数秒，默认大概不到3小时。
    sess.init_app(app=app)


# CKEditor配置
def init_ckeditor(app):
    ckeditor.init_app(app=app)


# uploads
def init_uploads(app):
    app.config['UPLOADS_DEFAULT_URL'] = '127.0.0.1:5000/'
    app.config['UPLOADS_DEFAULT_DEST'] = 'static/uploads'
    app.config['UPLOADED_PHOTO_ALLOW'] = IMAGES
    app.config['ALLOWED_EXTENSIONS'] = ['.jpg', '.jpeg', '.png', '.gif']
    configure_uploads(app, photos)
