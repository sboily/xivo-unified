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


from flask.ext.wtf import TextField, BooleanField, PasswordField, ValidationError, SelectField, RecaptchaField, html5, fields, validators, SubmitField, Required, QuerySelectField
from flask.ext.babel import lazy_gettext as _
from app.models import Organisations, User
from app.utils import Form

class AccountForm(Form):
    username = TextField(_('Username'), [Required(),
        validators.Length(min=3, max=20),
        validators.Regexp(r'^[^@:]*$', message=_("Username shouldn't contain '@' or ':'"))
    ])
    email = html5.EmailField(_('Email address'), [
        validators.Length(min=3, max=128),
        validators.Email(message=_("This should be a valid email address."))
    ])
    displayname = TextField(_('Display name'))
    password = PasswordField(_('Password'), [Required(),
        validators.Length(min=8, message=_("It's probably best if your password is longer than 8 characters."))
    ])
    role = SelectField(_('Role'), choices=[('300', 'Root'),('200', 'Manager'),('100', 'Admin')])
    submit = SubmitField(_('Save'))

    language = SelectField(_('Language'), choices=[('en', _('English')),('fr', _('French'))])

    organisations = QuerySelectField(_('Organisation'), get_label='name',query_factory=lambda: Organisations.query)


class SignupForm(Form):
    displayname = TextField(_('Display name'))

    username = TextField(_('Username'), [Required(),
        validators.Length(min=3, max=20),
        validators.Regexp(r'^[^@:]*$', message=_("Username shouldn't contain '@' or ':'"))
    ])
    email = html5.EmailField(_('Email address'), [Required(),
        validators.Length(min=3, max=128),
        validators.Email(message=_("This should be a valid email address."))
    ])
    password = PasswordField(_('Password'), [
        Required(),
        validators.Length(min=8, message=_("It's probably best if your password is longer than 8 characters.")),
        validators.EqualTo('confirm', message=_("Passwords must match."))
    ])
    confirm = PasswordField(_('Confirm password'))
    captcha = RecaptchaField(_('Captcha'))

    agree = BooleanField(_('I agree with the Terms and Conditions'))

    submit = SubmitField(_('Signup'))

    def validate_username(self, field):
        user = self.get_user()

        if user:
            raise ValidationError(_('Username already used'))

    def validate_email(self, field):
        email = self.get_email()

        if email:
            raise ValidationError(_('Email already used'))

    def get_user(self):
        return User.query.filter_by(username=self.username.data).first()

    def get_email(self):
        return User.query.filter_by(email=self.email.data).first()

