from flask import Flask, render_template, redirect, url_for, request
from flask_login import LoginManager, UserMixin, login_user, login_required, current_user, logout_user
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm, CSRFProtect
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Length
import bcrypt
import secrets


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
foo = secrets.token_urlsafe(16)
app.secret_key = foo
# Flask-WTF requires this line
csrf = CSRFProtect(app)

###### Modelos de base de datos ######

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)

    def __init__(self, username, name, password):
        self.username = username
        self.name = name
        self.password = password

    @classmethod
    def login (cls, username, password):
        user = cls.query.filter_by(username=username).first()
        if user:
            if bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
                return user
            else:
                return False
        else:
            return False 
        
    def hash_password(self):
        self.password = bcrypt.hashpw(self.password.encode('utf-8'), bcrypt.gensalt())
    
    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password)

###### Formularios ######
class LoginForm(FlaskForm):
    username = StringField('Username:', validators=[DataRequired(), Length(4, 10)])
    password = PasswordField('Password:', validators=[DataRequired(), Length(4, 15)])
    submit = SubmitField('Submit')

class RegisterForm(FlaskForm):
    username = StringField('Username:', validators=[DataRequired(), Length(4, 10)])
    name = StringField('Name:', validators=[DataRequired(), Length(10, 100)])
    password = PasswordField('Password:', validators=[DataRequired(), Length(4, 15)])
    submit = SubmitField('Submit')

class LogoutForm(FlaskForm):
    submit = SubmitField('Log Out')

###### Gestor de login ######
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

@app.route('/')
@login_required
def index():
    logout_form = LogoutForm()
    return render_template('index.html', logout_form=logout_form, current_user=current_user)


@app.route('/user-data')
def user_data():
    user_id = request.args.get('id')
    user = User.query.get(user_id)
    if user is None:
        return redirect(url_for('register'))
    return render_template('user_data.html', user=user)

@app.route('/register', methods=['GET', 'POST'])
def register():
    register_form = RegisterForm()
    if register_form.validate_on_submit():
        user = User(username=register_form.username.data, name=register_form.name.data, password=register_form.password.data)
        user.hash_password()
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('user_data', id=user.id))
    return render_template('register.html', register_form=register_form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        user = User.query.filter_by(username=login_form.username.data).first()
        if user is None:
            return redirect(url_for('register'))
        if user.check_password(login_form.password.data):
            # aca ya decidimos que el usuario es valido y la contraseña tambien
            print("Estado del Usuario: {}".format(current_user.is_active))
            login_user(user)
            print("Estado del Usuario: {}".format(current_user.is_active))
            #return redirect(url_for('user_data', id=user.id))
        return redirect(url_for('index'))
    return render_template('login.html', login_form=login_form)

@app.route('/logout', methods=['POST'])
@login_required
def logout():
    print("Estado del Usuario: {}".format(current_user.is_active))
    logout_user()
    print("Estado del Usuario: {}".format(current_user.is_active))
    return redirect(url_for('login'))

###### Creamos la base de datos con los modelos que le dimos ######
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
