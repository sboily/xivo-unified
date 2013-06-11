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


from flask.ext.wtf import Form, TextField, BooleanField, PasswordField, ValidationError, QuerySelectField, SubmitField, QuerySelectMultipleField
from flask.ext.wtf import Required, IPAddress, Regexp, validators
from models import Servers
from app.core.login.models import User
from flask.ext.babel import lazy_gettext as _
import re

def get_servers_list():
    return User.query.order_by(User.displayname)

class ServersForm(Form):
    name = TextField(_('Name'), [Required(),
        validators.Length(min=3, max=30),
        validators.Regexp(r'^[^@:]*$', message=_("Name shouldn't contain '@' or ':'"))
    ])

    address = TextField(_('Address'), [Required(), IPAddress()])
    login = TextField(_('Login'))
    password = PasswordField(_('Password'))

    users = QuerySelectMultipleField(_('Users'), get_label='displayname',query_factory=get_servers_list)

    submit = SubmitField(_('Submit'))
