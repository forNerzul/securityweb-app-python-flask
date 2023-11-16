from flask_login import UserMixin, login_user, logout_user
from security_guard_app.config import db
import bcrypt

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(100), nullable=False, default="user")

    def __init__(self, username, name, password, role):
        self.username = username
        self.name = name
        self.password = password
        self.role = role

    @classmethod
    def get_user_by_id(cls, user_id):
        return db.session.query(cls).filter_by(id=user_id).first()
    
    @classmethod
    def get_user_by_username(cls, username):
        return db.session.query(cls).filter_by(username=username).first()
    
    @classmethod
    def check_if_user_exists(cls, username):
        return db.session.query(db.exists().where(cls.username == username)).scalar()
    
    def has_role(self, role):
        return self.role == role
    
    def login(self):
        login_user(self)

    def logout(self):
        logout_user()
    
    def add_user_to_db(self):
        db.session.add(self)
        db.session.commit()

    def hash_password(self):
        self.password = bcrypt.hashpw(self.password.encode('utf-8'), bcrypt.gensalt())
    
    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password)
