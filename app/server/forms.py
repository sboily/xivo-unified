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


from flask.ext.wtf import Form, TextField, BooleanField, PasswordField, ValidationError
from flask.ext.wtf import Required
from models import Servers
import re

class ServersForm(Form):
    name = TextField('name', [Required()])
    address = TextField('address', [Required()])
    login = TextField('login')
    password = PasswordField('password')


    def validate_name(self, field):
        check_name = re.compile('^[a-zA-Z0-9\.]+$')
        if not re.search(check_name, field.data):
            raise ValidationError('Invalid Name')

    def validate_address(self, field):
        check_ip = re.compile('^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$')
        if not re.match(check_ip, field.data):
            raise ValidationError('Invalid Host')

    def validate_login(self, field):
        return

    def validate_password(self, field):
        return
