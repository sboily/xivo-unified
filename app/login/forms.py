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
from models import User

class LoginForm(Form):
    login = TextField('login', validators=[Required()])
    password = PasswordField('password', validators=[Required()])
    remember_me = BooleanField('remember_me', default=False)

#    def validate_login(self, field):
#        user = self.get_user()
#
#        if user is None:
#            raise ValidationError('Invalid user')
#
#        if user.password != self.password.data:
#            raise ValidationError('Invalid password')
#
#    def get_user(self):
#        return User(self.login.data, self.password.data)
