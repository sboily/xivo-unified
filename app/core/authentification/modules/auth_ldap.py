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
from flask.ext.principal import RoleNeed, UserNeed
from flask.ext.login import UserMixin
from ..plugins import Plugin

class AuthLdap(Plugin, UserMixin):
    def __init__(self):
        self.username = None
        self.passwd = None
        self.id = None
        self.organisation_id = 0
        self.role = 0
        self.language = 'en'
        self.displayname = 'Not set'
        self.active = 0

    def connect(self, host):
        connect = ldap.open(host)
        if connect:
            return connect
        return False

    def get_config(self):
        authldapserver = AuthServerLdap.query.first()
        if authldapserver:
            self.basedn = authldapserver.basedn
            self.searchfilter = authldapserver.searchfilter
            return authldapserver
        return None

    def authenticate(self, username, passwd):
        self.username = username
        self.passwd = passwd
        self.active = 0

        ldapconfig = self.get_config()
        if ldapconfig:
            searchfilter = ldapconfig.searchfilter +"="+ username
            userdn = searchfilter +","+ ldapconfig.basedn
        else:
            return self

        if ldapconfig.active:
            conn = self.connect(ldapconfig.host)
            if conn:
                user = self.auth_user(conn, userdn, passwd, searchfilter)
        else:
            print "LDAP backend is not activated"

        return self

    def auth_user(self, conn, userdn, passwd, searchfilter):
        try:
            conn.bind_s(userdn, passwd)
        except ldap.LDAPError:
            conn.unbind_s()
            return False

        result = conn.search_s(self.basedn, ldap.SCOPE_SUBTREE, searchfilter)
        conn.unbind_s()

        self.username = result[0][1]['uid'][0]
        self.id = unicode(result[0][1]['uidNumber'][0])
        self.displayname = result[0][1]['cn'][0]
        self.organisation_id = self.get_organisation_id(result[0][1]['o'][0])
        self.role = 50
        self.active = 1

        return True

    def get_organisation_id(self, organisation):
        org = Organisations.query.filter(Organisations.name == organisation).first()
        print org
        if org:
            return org.id

        return 0

    def is_activate(self):
        return True

    def get_user_by_id(self, id):
        if self.active and self.id == id:
            print 'LDAP id'
            return self
        return False

    def get_user_by_username(self, username):
        if self.active and username == self.username:
            print 'LDAP username'
            return self
        return False

    def from_identity(self, identity):
        if self.active:
            identity.provides.update(self.provides(self.username))
            return self

    def provides(self, userid):
        needs = [RoleNeed('authenticated'), UserNeed(userid)]
        needs.append(RoleNeed('user'))
        return needs

    def register_signals(self):
        print "Activating LDAP Auth"

class UserLdap(UserMixin):
    def __init__(self):
        pass

    def authenticate(self):
        return True
