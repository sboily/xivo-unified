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
        self.username = username
        self.passwd = passwd
        self.active = False

        is_sql = True
        is_ldap = False

        if is_sql:
            self.auth_sql()

        if is_ldap:
            self.auth_ldap()

    def auth_ldap(self):
       user = UserLdap(self.username, self.passwd)

       if user:
           self.id = user['id']
           self.active = True

    def auth_sql(self):
        user = UserSql(self.username, self.passwd)
        if user:
            self.active = True
            self.id = user.id

    def is_active(self):
        return self.active

    def get_id(self):
        return self.id
