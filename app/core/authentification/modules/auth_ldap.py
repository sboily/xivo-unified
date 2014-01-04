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
from flask.ext.login import UserMixin, current_user
from werkzeug.utils import cached_property
from ..plugins import Plugin

class AuthLdap(Plugin):
    def __init__(self):
        self.auth_type = "ldap"

    def connect(self, host):
        ldapobj = ldap.initialize("ldap://%s:389" % host, 0)
        ldapobj.set_option(ldap.OPT_TIMEOUT, 2)
        ldapobj.set_option(ldap.OPT_NETWORK_TIMEOUT, 2)
        ldapobj.set_option(ldap.OPT_REFERRALS, 0)
        if ldapobj:
            return ldapobj
        return False

    def bind(self, conn, user, passwd, with_simple=None):
        try:
            if with_simple:
                return conn.simple_bind(user, passwd)
            else:
                return conn.bind_s(user, passwd)
        except:
            print "Error on LDAP binding"

        conn.unbind_s()
        return False

    def search(self, conn, basedn, searchfilter):
        attrs = ['uid', 'o', 'uidNumber', 'cn', 'mail']
        return conn.search_s(basedn, ldap.SCOPE_SUBTREE, searchfilter, attrs)

    def authenticate(self, username=None, passwd=None, by_id=None, by_username=None):
        with_simple = False

        ldapconfig = self.get_config()
        if ldapconfig:
            host = ldapconfig.host
            basedn = ldapconfig.basedn

            if username:
                searchfilter = ldapconfig.searchfilter +"="+ username
                username = searchfilter +","+ ldapconfig.basedn

            if by_username:
                username = ldapconfig.login
                passwd = ldapconfig.passwd
                searchfilter = ldapconfig.searchfilter +"="+ by_username
                with_simple = True

            if by_id:
                username = ldapconfig.login
                passwd = ldapconfig.passwd
                searchfilter = "uidNumber=" + str(by_id)
                with_simple = True

            if ldapconfig.active:
                conn = self.connect(host)
                if self.bind(conn, username, passwd, with_simple):
                    result = self.search(conn, basedn, searchfilter)
                    conn.unbind_s()
                    if result:
                        return UserLdap(result)
        else:
            print "LDAP backend is not activated"

        return False

    def get_config(self):
        return AuthServerLdap.query.first()

    def search_by_id_or_username(self, id=None, username=None):
        return self.authenticate(by_username=username, by_id=id)

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

    def register_signals(self):
        print "Activating LDAP Auth"

class UserLdap(UserMixin):

    USER = 50
    ADMIN = 100
    MANAGER = 200
    ROOT = 300

    def __init__(self, result):
        self.id = int(result[0][1]['uidNumber'][0])
        self.username = unicode(result[0][1]['uid'][0], "UTF-8")
        self.displayname = unicode(result[0][1]['cn'][0], "UTF-8")
        self.email = unicode(result[0][1]['mail'][0], "UTF-8")
        self.organisation_id = self._get_organisation_id(result[0][1]['o'][0])
        self.organisation_name = unicode(result[0][1]['o'][0], "UTF-8")
        self.role = 50
        self.active = 1
        self.language = 'en'
        self.created_time = None

    def _get_organisation_id(self, organisation):
        id = 0
        org = Organisations.query.filter(Organisations.name == organisation).first()
        if org:
            return (int(org.id))

        return id

    def from_identity(self, identity):
        if identity.id == current_user.id:
            identity.provides.update(self.provides)
            identity.auth_type = "ldap"
        else:
            identity.auth_type = ""

    @cached_property
    def provides(self):
        needs = [RoleNeed('authenticated'), UserNeed(current_user.id)]

        if self.is_user:
            needs.append(RoleNeed('user'))

        if self.is_admin:
            needs.append(RoleNeed('admin'))

        if self.is_manager:
            needs.append(RoleNeed('manager'))

        if self.is_root:
            needs.append(RoleNeed('root'))

        return needs

    @property
    def is_user(self):
        return self.role == self.USER

    @property
    def is_admin(self):
        return self.role == self.ADMIN

    @property
    def is_manager(self):
        return self.role == self.MANAGER

    @property
    def is_root(self):
        return self.role == self.ROOT

    def __repr__(self):
        return "<%d : %s (%s)>" % (self.id, self.username, self.email)
