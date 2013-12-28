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

from werkzeug.security import generate_password_hash, check_password_hash
from app.models import User
from ..plugins import Plugin

class AuthSql(Plugin):
    def __init__(self):
        self.auth_type = "sql"

    def authenticate(self, username, passwd):
        user = User.query.filter_by(username=username).first()
        if user and self.check_passwd(user.password, passwd):
            return user
        return False

    def get_user_by_id(self, id):
        return User.query.filter_by(id=id).first()

    def get_user_by_username(self, username):
        return User.query.filter_by(username=username).first()

    def from_identity(self, identity):
        if identity.id and (not identity.auth_type or identity.auth_type == "sql"):
            return User.query.from_identity(identity)
        return False

    def check_passwd(self, sql_passwd, passwd):
        return check_password_hash(sql_passwd, passwd)

    def is_activate(self):
        return True

    def register_signals(self):
        print "Activating SQL Auth"
