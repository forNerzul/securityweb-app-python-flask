from flask_login import LoginManager

login_manager = LoginManager()
login_manager.login_view = 'app_views.login'

@login_manager.user_loader
def load_user(user_id):
    from security_guard_app.models.User import User
    return User.query.get(int(user_id))
