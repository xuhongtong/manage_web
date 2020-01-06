from flask import current_app, render_template
from flask_mail import Message
from threading import Thread

# 异步发送邮件
from apps.ext import mail


def async_send_mail(app, msg):
    # 必须在程序上下文中才能发送邮件，新建的线程没有，因此需要手动创建
    with app.app_context():
        # 发送邮件
        mail.send(msg)


# 封装函数发送邮件
def send_activate_mail(to, subject, template, **kwargs):
    # 获取原始的app实例
    app = current_app._get_current_object()
    # 创建邮件对象
    msg = Message(subject, recipients=[to], sender='jingyetong@163.com')
    # 浏览器接收显示内容
    msg.html = render_template('login/' + template + '.html', **kwargs)
    # 终端接收显示内容
    # msg.body = render_template('login/' + template + '.txt', **kwargs)
    # 创建线程，在新的线程中发送邮件
    thr = Thread(target=async_send_mail, args=[app, msg])
    thr.start()
    return thr


def send_reset_mail(to, subject, template, **kwargs):
    # 获取原始的app实例
    app = current_app._get_current_object()
    # 创建邮件对象
    msg = Message(subject, recipients=[to], sender='jingyetong@163.com')
    # 浏览器接收显示内容
    msg.html = render_template('login/' + template + '.html', **kwargs)
    # 终端接收显示内容
    # msg.body = render_template('login/' + template + '.txt', **kwargs)
    # 创建线程，在新的线程中发送邮件
    thr = Thread(target=async_send_mail, args=[app, msg])
    thr.start()
    return thr

# send_mail('end_moon@163.com', '账号激活', 'activate', username='tom')
