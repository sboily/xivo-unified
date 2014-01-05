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

from flask.ext.principal import RoleNeed, UserNeed
from flask.ext.login import UserMixin, current_user
from werkzeug.utils import cached_property

class UserAuth(UserMixin):

    USER = 50
    ADMIN = 100
    MANAGER = 200
    ROOT = 300

    def __init__(self, result):
        if not result:
            return None
        self.id = result['id']
        self.username = result['username']
        self.displayname = result['displayname']
        self.email = result['email']
        self.organisation_id = result['organisation_id']
        self.organisation_name = result['organisation_name']
        self.role = result['role']
        self.active = result['active']
        self.language = result['language']
        self.created_time = result['created_time']

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
