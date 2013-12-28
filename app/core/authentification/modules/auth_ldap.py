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

class AuthLdap(Plugin):
    def __init__(self):
        self.auth_type = "ldap"

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
        ldapconfig = self.get_config()
        if ldapconfig:
            searchfilter = ldapconfig.searchfilter +"="+ username
            userdn = searchfilter +","+ ldapconfig.basedn
        else:
            return False

        if ldapconfig.active:
            conn = self.connect(ldapconfig.host)
            if conn:
                user = UserLdap(conn, self.basedn, searchfilter)
                if user.authenticate(userdn, passwd):
                    return user
        else:
            print "LDAP backend is not activated"

        return False

    def search_by_id_or_username(self, id=None, username=None):
        if id:
            searchfilter = "uidNumber=" + str(id)
        if username:
            searchfilter = "uid=" + username

        is_active = False
        ldapconfig = self.get_config()
        if ldapconfig:
            login = ldapconfig.login
            passwd = ldapconfig.passwd
            basedn = ldapconfig.basedn
            host = ldapconfig.host
            is_active = ldapconfig.active

        if is_active:
            conn = self.connect(host)
            user = UserLdap(conn, basedn, searchfilter)
            if user.authenticate(login, passwd, True):
                return user

        return False

    def is_activate(self):
        return True

    def get_user_by_id(self, id):
        if id.isnumeric():
            return self.search_by_id_or_username(id=id)
        return False

    def get_user_by_username(self, username):
        if username is not None:
            return self.search_by_id_or_username(username=username)
        return False

    def from_identity(self, identity):
        if identity.id and (not identity.auth_type or identity.auth_type == "ldap"):
            user = self.search_by_id_or_username(id=identity.id)
            if user:
                identity.provides.update(self.provides(identity.id))
                identity.auth_type = "ldap"
                return user
            else:
                identity.auth_type = ""
        return False

    def provides(self, userid):
        needs = [RoleNeed('authenticated'), UserNeed(userid)]
        needs.append(RoleNeed('user'))
        return needs

    def register_signals(self):
        print "Activating LDAP Auth"

class UserLdap(UserMixin):
    def __init__(self, conn, basedn, searchfilter):
        self.conn = conn
        self.basedn = basedn
        self.searchfilter = searchfilter
        self.id = None
        self.organisation_id = None
        self.role = None
        self.language = 'en'
        self.displayname = 'Not set'
        self.active = 0
        self.attrs = ['uid', 'o', 'uidNumber', 'cn']

    def authenticate(self, user, passwd, with_auth_ldap=None):
        if self.bind(user, passwd, with_auth_ldap):
            return self.search()
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

    def search(self):
        result = self.conn.search_s(self.basedn, ldap.SCOPE_SUBTREE, self.searchfilter, self.attrs)
        self.conn.unbind_s()

        if not result:
            return False

        self.username = result[0][1]['uid'][0]
        self.id = unicode(result[0][1]['uidNumber'][0])
        self.displayname = result[0][1]['cn'][0]
        self.organisation_id = self._get_organisation_id(result[0][1]['o'][0])
        self.role = 50
        self.active = 1

        return self

    def _get_organisation_id(self, organisation):
        organisation_id = 0
        org = Organisations.query.filter(Organisations.name == organisation).first()
        if org:
            organisation_id = org.id

        return organisation_id
