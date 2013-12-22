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


from wtforms.fields import TextField, BooleanField, PasswordField, SelectField, SubmitField
from wtforms.validators import Required, ValidationError
from flask.ext.babel import lazy_gettext as _
from app.models import User
from app.utils import Form

class LoginForm(Form):
    username = TextField(_('Username'), validators=[Required()])
    password = PasswordField(_('Password'), validators=[Required()])
    remember_me = BooleanField(_('Remember me'), default=False)

    language = SelectField(_('Language'), choices=[('en', _('English')),('fr', _('French'))])

    submit = SubmitField(_('Sign in'))

    def validate_login(self, field):
        user = self.get_user()

        if user is None:
            raise ValidationError(_('Invalid user'))

    def validate_password(self, field):
        user = self.get_user()

        if user is None:
            raise ValidationError(_('Invalid user'))

        if not User.check_password(user, self.password.data):
            raise ValidationError(_('Invalid password'))

    def get_user(self):
        return User.query.filter_by(username=self.username.data).first()

class AuthServerLdapForm(Form):
    host = TextField(_('LDAP host'), [Required()])
    basedn = TextField(_('Base DN'), [Required()])
    searchfilter = TextField(_('Search filter'), [Required()])
    active = BooleanField(_('Enable LDAP auth'), default=False)
    submit = SubmitField(_('Save'))
