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
from flask import session
import inspect

debug_auth = False

def authenticate(username, password):
    return _call('authenticate', username, password)

def get_user_by_id(id):
    return _call('get_user_by_id', id)

def get_user_by_username(username):
    return _call('get_user_by_username', username)

def check_password():
    return True

def _call(method, *args):
    for plugin in Plugin.plugins:
        auth_type = session.get('identity.auth_type', None)
        if plugin.auth_type == auth_type or auth_type == None:
            call = getattr(plugin, method)
            user = call(*args)
            _debug(plugin, user, *args)
            if user is not False:
                return user
    return False

def _debug(plugin, user , *args):
    if debug_auth:
        print "############ DEBUG ##################"
        print "From function : ", inspect.stack()[1][3]
        print "Backend : ", plugin.__module__
        print "Authenticate :", dir(user)
        print "Arguments : ", args
        print "Return : ", user
        print "Session : ", session
        print "####################################"
