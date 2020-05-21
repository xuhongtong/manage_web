from functools import wraps
from io import BytesIO
from operator import and_
from flask import redirect, url_for, request, Blueprint, flash, make_response
from sqlalchemy import or_
from apps.auth.models import User
from flask import render_template
from flask import session
from apps.ext import db
from apps.utils.captcha import get_verify_code
from apps.utils.mail import send_activate_mail, send_reset_mail
import hashlib

user = Blueprint('user', __name__, template_folder='templates', static_folder='static')


# md5加密
def my_md5(s, salt=''):
    s += salt
    news = str(s).encode()
    m = hashlib.md5(news)
    return m.hexdigest()


# 访问前验证是否登录
def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if session.get('username'):
            return func(*args, **kwargs)
        else:
            return redirect(url_for('user.login', next=request.url))

    return wrapper


# 登录检验（用户名、密码是否正确）
def is_vaild_login(username, password):
    user = User.query.filter(and_(User.username == username, User.password == my_md5(password))).first()
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


# 验证码
@user.route('/code')
def get_code():
    session.pop('image', None)
    image, str = get_verify_code()
    # 将验证码图片以二进制形式写入在内存中，防止将图片都放在文件夹中，占用大量磁盘
    buf = BytesIO()
    image.save(buf, 'jpeg')
    buf_str = buf.getvalue()
    # 把二进制作为response发回前端，并设置首部字段
    response = make_response(buf_str)
    response.headers['Content-Type'] = 'image/gif'
    # 将验证码字符串储存在session中
    session['image'] = str
    return response


@user.route('/')
@login_required
def home():
    return render_template('login/index.html')


# 登录
@user.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if is_vaild_login(request.form.get('username'), request.form.get('password')):
            if is_active_login(request.form.get('username')):
                # 是否勾选记住账号
                if request.form.get('remember'):
                    session['remember_username'] = request.form['username']
                    session['is_remember'] = 'on'
                else:
                    session.pop('is_remember', None)
                    session.pop('remember_username', None)
                # 取验证码
                if session.get('image'):
                    if session.get('image').lower() == request.form.get('captcha'):
                        flash("成功登录！")
                        session['username'] = request.form.get('username')
                        return redirect(url_for('blogadmin.article'))
                    else:
                        error = '验证码错误'
                else:
                    error = '请输入验证码'

            else:
                error = '账号未激活！'
        else:
            error = '账号或密码错误!'
    content = {
        'error': error,
        'username': request.form.get('username'),
        'remember_username': session.get('remember_username'),
        'is_remember': session.get('is_remember')
    }
    return render_template('login/login.html', **content)

# 注销
@user.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('user.home'))


# 注册
@user.route('/register', methods=['GET', 'POST'])
def register():
    error = None
    if request.method == 'POST':
        db.create_all()
        if request.form['password1'] != request.form['password2']:
            error = '两次密码不相同！'
        elif valid_register(request.form['username'], request.form['email']):
            user = User(username=request.form['username'], password=my_md5(request.form['password1']),
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
