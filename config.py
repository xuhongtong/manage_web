import os

basedir = os.path.abspath(os.path.dirname(__file__))
WHOOSH_BASE = os.path.join(basedir, 'WHOOSH_BASE_INDEX')

media_base=os.path.join(basedir, 'static/uploads/')


mysql_info = {
    'username': 'root',
    'password': '123456',
    'host': '192.168.199.130',
    'port': '3306',
    'database': 'web'
}


MAIL_USERNAME='jingyetong@163.com'
MAIL_PASSWORD='jinye123'