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

def UserLdap(username, passwd):
    uid = ""
    ldapsrv = ""
    basedn = ""

    try:
        if username and passwd:
            l = simpleldap.Connection(ldapsrv,
                dn='uid={0},{1}'.format(username, basedn), password=passwd)
            r = l.search('uid={0}'.format(username), base_dn=basedn)
        else:
            l = simpleldap.Connection(ldapsrv)
            r = l.search('uidNumber={0}'.format(uid), base_dn=basedn)

        return { 'name': r[0]['uid'][0],
                 'id': unicode(r[0]['uidNumber'][0])
               }
    except:
        return None
