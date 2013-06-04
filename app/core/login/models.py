# -*- coding: utf-8 -*-

# Copyright (C) 2013 Sylvain Boily <sboily@proformatique.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


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
