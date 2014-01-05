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
from app.models import AuthServerLdap, Organisations
from ..plugins import Plugin
from auth_base import UserAuth

class AuthLdap(Plugin):
    def __init__(self):
        self.auth_type = "ldap"
        self.username = None
        self.passwd = None
        self.by_id = None
        self.by_username = None
        self.conn = None

    def connect(self, host):
        ldapobj = ldap.initialize("ldap://%s:389" % host, 0)
        ldapobj.set_option(ldap.OPT_TIMEOUT, 2)
        ldapobj.set_option(ldap.OPT_NETWORK_TIMEOUT, 2)
        ldapobj.set_option(ldap.OPT_REFERRALS, 0)
        if ldapobj:
            return ldapobj
        return False

    def bind(self, user, passwd, with_simple=None):
        try:
            if with_simple:
                return self.conn.simple_bind(user, passwd)
            else:
                return self.conn.bind_s(user, passwd)
        except:
            print "Error on LDAP binding"

        self.conn.unbind_s()
        return False

    def search(self, basedn, searchfilter):
        attrs = ['uid', 'o', 'uidNumber', 'cn', 'mail']
        return self.conn.search_s(basedn, ldap.SCOPE_SUBTREE, searchfilter, attrs)

    def authenticate(self, username, passwd):
        self.username = username
        self.passwd = passwd
        return self.search_user()

    def search_user(self):
        config = self.set_config()
        if config['active']:
            self.conn = self.connect(config['host'])
            if self.bind(config['username'], config['passwd'], config['with_simple']):
                result = self.search(config['basedn'], config['searchfilter'])
                self.conn.unbind_s()
                if result:
                    user = self.parse_result(result)
                    return UserAuth(user)
        else:
            print "LDAP backend is not activated"

        return False

    def set_config(self):
        ldapconfig = self.get_config_from_db()
        if ldapconfig:
            config = { 'host': ldapconfig.host,
                       'basedn' : ldapconfig.basedn,
                       'searchfilter': None,
                       'username': None,
                       'passwd': self.passwd,
                       'with_simple': False,
                       'active' : ldapconfig.active
                     }

            if self.username:
                searchfilter = ldapconfig.searchfilter
                config['searchfilter'] = searchfilter +"="+ self.username
                config['username'] = config['searchfilter'] +","+ ldapconfig.basedn
                self.username = None
                self.passwd = None

            if self.by_username:
                config['username'] = ldapconfig.login
                config['passwd'] = ldapconfig.passwd
                config['searchfilter'] = ldapconfig.searchfilter +"="+ self.by_username
                config['with_simple'] = True
                self.by_username = None

            if self.by_id:
                config['username'] = ldapconfig.login
                config['passwd'] = ldapconfig.passwd
                config['searchfilter'] = "uidNumber=" + str(self.by_id)
                config['with_simple'] = True
                self.by_id = None

            return config

    def get_config_from_db(self):
        return AuthServerLdap.query.first()

    def is_activate(self):
        return True

    def get_user_by_id(self, id):
        if id.isnumeric():
            self.by_id = id
            return self.search_user()
        return False

    def get_user_by_username(self, username):
        if username is not None:
            self.by_username = username
            return self.search_user()
        return False

    def parse_result(self, result):
        user = {'id': int(result[0][1]['uidNumber'][0]),
                'username': unicode(result[0][1]['uid'][0], "UTF-8"),
                'displayname': unicode(result[0][1]['cn'][0], "UTF-8"),
                'email': unicode(result[0][1]['mail'][0], "UTF-8"),
                'organisation_id': self._get_organisation_id(result[0][1]['o'][0]),
                'organisation_name': unicode(result[0][1]['o'][0], "UTF-8"),
                'role': 50,
                'active': 1,
                'language': 'en',
                'created_time': None,
               }

        return user

    def _get_organisation_id(self, organisation):
        id = 0
        org = Organisations.query.filter(Organisations.name == organisation).first()
        if org:
            return (int(org.id))

        return id

    def register_signals(self):
        print "Activating LDAP Auth"
