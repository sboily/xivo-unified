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

from plugins import Plugin

def authenticate(username, password):
    for plugin in Plugin.plugins:
        print "Backend : ", plugin.__module__
        user = plugin.authenticate(username, password)
        print "Authenticate :", dir(user)
        print "Is user is activate : ", user.active
        print "####################################"
        if user.active:
            return user

def get_user_by_id(id):
    for plugin in Plugin.plugins:
        user = plugin.get_user_by_id(id)
        if user:
            return user

def get_user_by_username(username):
    for plugin in Plugin.plugins:
        user = plugin.get_user_by_username(username)
        if user:
            return user

def from_identity(identity):
    for plugin in Plugin.plugins:
        user = plugin.from_identity(identity)
        if user:
            return user

def check_password():
    return True
