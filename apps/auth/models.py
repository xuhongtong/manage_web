from flask import current_app

from apps.ext import db
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer


class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(80))
    email = db.Column(db.String(120), unique=True)
    is_vaild = db.Column(db.Boolean, default=0)

    def generate_activate_token(self, expires_in=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expires_in=expires_in)
        return s.dumps({'id': self.id})

    @staticmethod
    def check_activate_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        u = User.query.get(data['id'])
        if not u:
            # 用户已被删除
            return False
        # 没有激活时才需要激活
        if not u.is_vaild:
            u.is_vaild = 1
            db.session.add(u)
            db.session.commit()
        return True

    @staticmethod
    def reset_password(token, password):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        u = User.query.get(data['id'])
        if not u:
            # 用户已被删除
            return False
        else:
            u.password = password
            db.session.commit()
            return True

    def __repr__(self):
        return '<User %r>' % self.username

# db.create_all()
# # 创建表格、插入数据
# @app.before_first_request
# def create_db():
#     db.drop_all()  # 每次运行，先删除再创建
#     db.create_all()
#
#     admin = User(username='admin', password='root', email='admin@example.com', is_vaild=1)
#     db.session.add(admin)
#
#     guestes = [User(username='guest5', password='guest1', email='guest1@example.com', is_vaild=1),
#                User(username='guest6', password='guest2', email='guest2@example.com', is_vaild=1),
#                User(username='guest7', password='guest3', email='guest3@example.com', is_vaild=1),
#                User(username='guest8', password='guest4', email='guest4@example.com', is_vaild=1)]
#     db.session.add_all(guestes)
#     db.session.commit()


# create_db()
