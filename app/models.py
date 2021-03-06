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


from werkzeug.security import generate_password_hash
from werkzeug.utils import cached_property
from flask.ext.login import UserMixin
from flask.ext.principal import RoleNeed, UserNeed
from flask.ext.sqlalchemy import BaseQuery
from datetime import datetime
from app.extensions import db

users_server = db.Table('users_server',
    db.Column('server_id', db.Integer, db.ForeignKey('servers.id')),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'))
)

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(200), unique=True)
    password = db.Column(db.String(200))
    email = db.Column(db.String(200), unique=True)
    displayname = db.Column(db.String(200))
    language = db.Column(db.String(10), default='en')
    role = db.Column(db.Integer, default=300)
    created_time = db.Column(db.DateTime, default=datetime.utcnow)
    organisation_id = db.Column(db.Integer, db.ForeignKey('organisations.id'))

    def __init__(self, username, password, email, displayname, role):
        self.email = email.lower()
        self.username = username
        self.password = generate_password_hash(password)
        self.displayname = displayname
        self.role = role

    def __repr__(self):
        return "<%d : %s (%s)>" % (self.id, self.username, self.email)


class Organisations(db.Model):
    __tablename__ = 'organisations'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    domain = db.Column(db.String(300))
    description = db.Column(db.Text())
    created_time = db.Column(db.DateTime, default=datetime.utcnow)
    organisation_id = db.Column(db.Integer, db.ForeignKey('organisations.id'))
    users = db.relationship('User', backref='organisations',lazy='dynamic')
    servers = db.relationship('Servers', backref='organisations',lazy='dynamic')
    plugins = db.relationship('Plugins', backref='organisation',lazy='dynamic')

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "<%d : %s>" % (self.id, self.name)

class Servers(db.Model):
    __tablename__ = 'servers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    address = db.Column(db.String(200))
    login = db.Column(db.String(200))
    password = db.Column(db.String(200))
    created_time = db.Column(db.DateTime, default=datetime.utcnow)
    organisation_id = db.Column(db.Integer, db.ForeignKey('organisations.id'))
    users = db.relationship('User', secondary=users_server, backref='servers')
    plugins = db.relationship('Plugins', backref='servers',lazy='dynamic')
    protocol = db.Column(db.String(200), default='1.1')

    def __init__(self, name, address, login=None, password=None):
        self.name = name
        self.address = address
        self.login = login
        self.password = password

    def __repr__(self):
        return "<%d : %s (%s)>" % (self.id, self.name, self.address)

class Plugins(db.Model):
    __tablename__ = 'plugins'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    installed_time = db.Column(db.DateTime, default=datetime.utcnow)
    organisation_id = db.Column(db.Integer, db.ForeignKey('organisations.id'))
    user_id = db.Column(db.Integer)
    server_id = db.Column(db.Integer, db.ForeignKey('servers.id'))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "<%d : name=%s org=%s serv=%s>" % (self.id, self.name, self.organisation_id, self.server_id)

class AuthServerLdap(db.Model):
    __tablename__ = 'auth_server_ldap'
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.Text())
    passwd = db.Column(db.Text())
    host = db.Column(db.Text())
    basedn = db.Column(db.Text())
    searchfilter = db.Column(db.Text())
    active = db.Column(db.Boolean)
    created_time = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "<%d : %s>" % (self.id, self.name)
