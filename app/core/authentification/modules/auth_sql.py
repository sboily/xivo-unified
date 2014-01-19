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
from app.models import User, Organisations
from ..plugins import Plugin
from auth_base import UserAuth

class AuthSql(Plugin):
    def __init__(self):
        self.auth_type = "sql"

    def authenticate(self, username, passwd):
        u = User.query.filter_by(username=username).first()
        if u:
            user = UserAuth(self.parse_result(u))
            if user and self.check_passwd(user.password, passwd):
                return user
        return False

    def get_user_by_id(self, id):
        u = User.query.filter_by(id=id).first()
        return UserAuth(self.parse_result(u))

    def get_user_by_username(self, username):
        u = User.query.filter_by(username=username).first()
        if u:
            return UserAuth(self.parse_result(u))
        return False

    def parse_result(self, result):
        user = False
        if result:
            user = {'id': result.id,
                    'username': result.username,
                    'displayname': result.displayname,
                    'email': result.email,
                    'organisation_id': result.organisation_id,
                    'organisation_name': self._get_organisation_name(result.organisation_id),
                    'organisation_domain': self._get_organisation_domain(result.organisation_id),
                    'role': result.role,
                    'active': 1,
                    'language': result.language,
                    'created_time': result.created_time,
                    'password': result.password,
                    'backend': "sql"
                   }

        return user

    def _get_organisation_name(self, id):
        name = None
        org = Organisations.query.filter(Organisations.id == id).first()
        if org:
            return org.name

        return name

    def _get_organisation_domain(self, id):
        dns = None
        org = Organisations.query.filter(Organisations.id == id).first()
        if org:
            return org.domain

        return dns

    def check_passwd(self, sql_passwd, passwd):
        return check_password_hash(sql_passwd, passwd)

    def is_activate(self):
        return True

    def register_signals(self):
        print "Activating SQL Auth"
