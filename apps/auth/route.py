from apps.auth.views import user


# 注册认证蓝图
def create_auth__register_blueprint(app):
    app.register_blueprint(user, prefix_url='/')
    app.register_blueprint(user, prefix_url='/login', endpoint='home')
    return app


# 注册全局蓝图
def create_register_blueprint(app):
    create_auth__register_blueprint(app)
