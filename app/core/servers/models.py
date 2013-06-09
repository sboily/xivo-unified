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
    users = db.relationship('UsersServer', backref='server', lazy = 'dynamic')

    def __init__(self, name, address, login=None, password=None):
        self.name = name
        self.address = address
        self.login = login
        self.password = password

    def __repr__(self):
        return "<%d : %s (%s)>" % (self.id, self.name, self.address)

class UsersServer(db.Model):
    __tablename__ = 'users_server'
    id = db.Column(db.Integer, primary_key=True)
    server_id = db.Column(db.Integer, db.ForeignKey('servers.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return "<%d : serv=%d user=%d>" % (self.id, self.server_id, self.user_id)
