# import hashlib
#
#
# def my_md5(s,salt=''):
#     s+=salt
#     news=str(s).encode()
#     m=hashlib.md5(news)
#     return m.hexdigest()
#
#
# print(my_md5(123)=='202cb962ac59075b964b07152d234b70')
