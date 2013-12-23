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

import ldap
from app.models import AuthServerLdap

class UserLdap(object):
    def __init__(self, username, passwd):
        self.username = username
        self.passwd = passwd
        self.authldapserver = AuthServerLdap.query.first()

    def auth(self):
        if self.authldapserver:
            basedn = self.authldapserver.basedn
            searchfilter = self.authldapserver.searchfilter +"="+ self.username
            userdn = searchfilter +","+ basedn
        else:
            return None

        connect = ldap.open(self.authldapserver.host)
        try:
            connect.bind_s(userdn, self.passwd)
            result = connect.search_s(basedn, ldap.SCOPE_SUBTREE, searchfilter)
            connect.unbind_s()
            result = { 'username': result[0][1]['uid'][0],
                       'id': unicode(result[0][1]['uidNumber'][0])
                     }
            return result
        except ldap.LDAPError:
            connect.unbind_s()
            return None

    def is_active(self):
        return self.authldapserver.active
