# encoding: utf8
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'user'
    id        = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email     = db.Column(db.Unicode(128), unique=True, nullable=False)
    password  = db.Column(db.Unicode(128))
    is_active = db.Column(db.Boolean, default=True)
    is_admin  = db.Column(db.Boolean, default=False)

    def __init__(self, *args, **kw):
        super(User, self).__init__(*args, **kw)
        self._authenticated = False


    def set_email(self, email):
        self.email = email


    def set_password(self, password):
        self.password = generate_password_hash(password)


    @property
    def is_authenticated(self):
        return self._authenticated


    def authenticate(self, password):
        print(password, " ", self.password)
        checked = check_password_hash(self.password, password)
        self._authenticated = checked
        return self._authenticated

    def get_id(self):
        return self.id

    def get_email(self):
        return self.email
