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

def UserLdap(username, passwd):
    authldapserver = AuthServerLdap.query.first()
    if authldapserver:
        basedn = authldapserver.basedn
        searchfilter = authldapserver.searchfilter +"="+ username
        userdn = searchfilter +","+ basedn

    else:
        return None

    connect = ldap.open(authldapserver.host)
    try:
        connect.bind_s(userdn, password)
        result = connect.search_s(basedn, ldap.SCOPE_SUBTREE, searchfilter)
        connect.unbind_s()
        print result
        result = { 'name': result[0]['uid'][0],
                   'id': unicode(result[0]['uidNumber'][0])
                 }
        return result
    except ldap.LDAPError:
        connect.unbind_s()
        print "authentication error"
        return None
