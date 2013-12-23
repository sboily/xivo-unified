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

from flask.ext.login import UserMixin
from auth_ldap import UserLdap
from auth_sql import UserSql

class Auth(UserMixin):
    def __init__(self, username=None, passwd=None):
        self.username = None
        self.passwd = False
        self.id = None
        self.active = False

        self.userldap = UserLdap(username, passwd)
        self.usersql = UserSql(username, passwd)

        is_sql = True
        is_ldap = self.userldap.is_active()

        if is_sql:
            if self.auth_sql():
                return None

        if is_ldap:
            if self.auth_ldap():
                return None

    def auth_ldap(self):
        user = self.userldap.auth()
        if user:
            self.username = user['username']
            self.id = user['id']
            self.active = True
            self.passwd = True
            return True
        return False

    def auth_sql(self):
        user = self.usersql.auth()
        if user:
            self.username = user.username
            self.id = user.id
            self.active = True
            self.passwd = True
            return True
        return False

    def is_active(self):
        return self.active

    def get_id(self):
        return self.id

    def get_user(self):
        return self.username

    def check_password(self):
        return self.passwd
