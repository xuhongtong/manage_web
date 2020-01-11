from apps.auth.views import user


# 注册认证蓝图
def create_auth__register_blueprint(app):
    app.register_blueprint(user, prefix_url='/')
    app.register_blueprint(user, prefix_url='/login', endpoint='home')
    return app



