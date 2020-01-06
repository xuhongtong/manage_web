from functools import wraps
from operator import and_
from flask import redirect, url_for, request, Blueprint, flash, session
from sqlalchemy import or_
from apps.auth.models import User
from flask import render_template

from apps.ext import db
from apps.utils.mail import send_activate_mail, send_reset_mail

user = Blueprint('user', __name__, template_folder='templates', static_folder='static')


# 访问前验证是否登录
def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # if g.user:
        if session.get('username'):
            return func(*args, **kwargs)
        else:
            return redirect(url_for('user.login', next=request.url))

    return wrapper


# 登录检验（用户名、密码是否正确）
def is_vaild_login(username, password):
    user = User.query.filter(and_(User.username == username, User.password == password)).first()
    if user:
        return True
    else:
        return False


# 登录检验（用户名、密码是否激活）
def is_active_login(username):
    user = User.query.filter(and_(User.username == username, User.is_vaild == 1)).first()
    if user:
        return True
    else:
        return False


# 注册检验（用户名、邮箱验证）
def valid_register(username, email):
    user = User.query.filter(or_(User.username == username, User.email == email)).first()
    if user:
        return False
    else:
        return True


@user.route('/')
@login_required
def home():
    return render_template('login/index.html', username=session.get('username'))


# # 2.登录
@user.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if is_vaild_login(request.form['username'], request.form['password']):
            if is_active_login(request.form['username']):
                flash("成功登录！")
                print('登录成功')
                print(request.form.get('username'))
                session['username'] = request.form.get('username')
                print(session.get('username'))
                session.permanent = True  #
                return redirect(url_for('user.home'))
            else:
                error = '账号未激活！'
        else:
            error = '账号或密码错误'
    return render_template('login/login.html', error=error)


# 3.注销
@user.route('/logout')
def logout():
    session.pop('username', None)
    # session.clear()
    return redirect(url_for('user.home'))


# # 4.注册
@user.route('/register', methods=['GET', 'POST'])
def register():
    error = None
    if request.method == 'POST':
        if request.form['password1'] != request.form['password2']:
            error = '两次密码不相同！'
        elif valid_register(request.form['username'], request.form['email']):
            user = User(username=request.form['username'], password=request.form['password1'],
                        email=request.form['email'])
            db.session.add(user)
            db.session.commit()
            token = user.generate_activate_token()
            send_activate_mail(user.email, '账号激活', 'activate', username=user.username, token=token)
            flash("成功注册,请移步至邮箱点击激活")
            return redirect(url_for('user.home'))
        else:
            error = '该用户名或邮箱已被注册！'

    return render_template('login/register.html', error=error)


@user.route('/activate/<token>')
def activate(token):
    if User.check_activate_token(token):
        flash('激活成功')
        return redirect(url_for('user.login'))
    else:
        flash('激活失败')
        return redirect(url_for('user.home'))


# 重置密码
@user.route('/forget', methods=['GET', 'POST'])
def forget():
    if request.method == 'POST':
        user = User.query.filter(User.email == request.form['email']).first()
        token = user.generate_activate_token()
        send_reset_mail(user.email, '重置密码', 'reset_password', username=user.username, token=token)
        flash('重置密码的邮件已经发送，请查收！')
        return redirect(url_for('user.login'))
    return render_template('login/forgot.html')


# 设置新密码
@user.route('/reset/<token>', methods=['GET', 'POST'])
def reset(token):
    if request.method == 'POST':
        if session.get('username'):
            return redirect(url_for('user.home'))
        if User.reset_password(token, request.form['password']):
            flash('您的密码已经修改成功')
            return redirect(url_for('user.login'))
    return render_template('login/reset.html', token=token)
