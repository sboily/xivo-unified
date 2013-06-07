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


from app import db
from datetime import datetime

class Servers(db.Model):
    __tablename__ = 'servers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    address = db.Column(db.String(200))
    login = db.Column(db.String(200))
    password = db.Column(db.String(200))
    created_time = db.Column(db.DateTime, default=datetime.utcnow)
    #users = db.relationship('UsersServer', uselist=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users_server.id'))
    user = db.relationship("UsersServer")

    def __init__(self, name, address, login=None, password=None, users=None):
        self.name = name
        self.address = address
        self.login = login
        self.password = password
        self.users = users

    def __repr__(self):
        return "<%d : %s (%s)>" % (self.id, self.name, self.address)

class UsersServer(db.Model):
    __tablename__ = 'users_server'
    id = db.Column(db.Integer, primary_key=True)
    server_id = db.Column(db.Integer)
    #user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

