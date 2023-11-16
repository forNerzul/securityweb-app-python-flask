#Project Flask MVC
from flask_wtf import CSRFProtect
from security_guard_app.config import Config, db, login_manager
from security_guard_app import app
from security_guard_app.router import app_views
import secrets


__author__ = "forNerzul"
__version__ = "1"
__email__ = "sbeardman92@gmail.com"


app.config.from_object(Config)
db.init_app(app)
app.register_blueprint(app_views)
app.secret_key = secrets.token_urlsafe(16)
login_manager.init_app(app)
# Flask-WTF requires this line
csrf = CSRFProtect(app)


# change template folder
app.template_folder = 'views'

# create database
with app.app_context():
    db.create_all()

# run app
if __name__ == '__main__':
    app.run( port=5000, debug=True)