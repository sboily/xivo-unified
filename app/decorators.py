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


from flask.ext.login import current_user
from flask import current_app
from functools import wraps

def required_role(role):
    """ Gatekeeper for views

This decorator checks that a user is authenticated
and that they have the required role to access a
view. If either check fails, they are sent
to the current app's login_managers unauthorized
route.

"""

    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if current_user.is_authenticated():
                if role in [x.name for x in current_user.roles]:
                    return f(*args, **kwargs)
            return current_app.login_manager.unauthorized()
        return decorated_function
    return decorator
