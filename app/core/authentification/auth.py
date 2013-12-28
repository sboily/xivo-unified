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
import inspect

_debug = True

def authenticate(username, password):
    for plugin in Plugin.plugins:
        user = plugin.authenticate(username, password)
        _debug(plugin, user, username, password)
        if user is not False:
            return user
    return False

def get_user_by_id(id):
    for plugin in Plugin.plugins:
        user = plugin.get_user_by_id(id)
        _debug(plugin, user, id)
        if user is not False:
            return user

def get_user_by_username(username):
    for plugin in Plugin.plugins:
        user = plugin.get_user_by_username(username)
        _debug(plugin, user, username)
        if user is not False:
            return user

def from_identity(identity):
    for plugin in Plugin.plugins:
        user = plugin.from_identity(identity)
        _debug(plugin, user, identity)
        if user is not False:
            return user

def check_password():
    return True

def _debug(plugin, user , *args):
    if _debug:
        print "############ DEBUG ##################"
        print "From function : ", inspect.stack()[1][3]
        print "Backend : ", plugin.__module__
        print "Authenticate :", dir(user)
        print "Arguments : ", args
        print "Return : ", user
        print "####################################"
