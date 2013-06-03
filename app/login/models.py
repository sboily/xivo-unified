from flask import current_app
from flask.ext.login import UserMixin
from app import db
from werkzeug.security import generate_password_hash, check_password_hash

roles = db.Table('roles',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer, db.ForeignKey('role.id'))
)

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(200), unique=True)
    password = db.Column(db.String(200))
    email = db.Column(db.String(200), unique=True)
    role = db.Column(db.SmallInteger, default=0)
    roles = db.relationship('Role', secondary=roles,
        backref=db.backref('users', lazy='dynamic'))

    def has_role(self,role_name):
        if role_name in [x.name for x in self.roles]:
            return True
        return False

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __init__(self, email, username, password):
        self.email = email.lower()
        self.username = username
        self.password = generate_password_hash(password)

    def __repr__(self):
        return "<%d : %s (%s)>" % (self.id, self.username, self.email)

class Role(db.Model):
    __tablename__ = 'role'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    name = db.Column(db.String(200))

    def __init__(self,name):
        self.name = name

    def __repr__(self):
        return '<{name}>'.format(name=self.name)
