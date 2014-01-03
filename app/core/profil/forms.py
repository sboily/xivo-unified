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
from wtforms.fields.html5 import EmailField
from wtforms.validators import ValidationError, Required, Length, Regexp, EqualTo, Email
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from flask.ext.wtf import RecaptchaField
from flask.ext.babel import lazy_gettext as _
from flask.ext.login import current_user
from app.models import Organisations, User
from app.utils import Form

ROOT = 300
MANAGER = 200
ADMIN = 100
USER = 50

def get_organisations():
    if current_user.is_root:
        return Organisations.query.all()
    else:
        return Organisations.query.filter(Organisations.id == current_user.organisation_id).all()

class AccountForm(Form):
    username = TextField(_('Username'), [Required(),
                                         Length(min=3, max=20),
                                         Regexp(r'^[^@:]*$', message=_("Username shouldn't contain '@' or ':'"))
                                        ])
    email = EmailField(_('Email address'), [
        Length(min=3, max=128),
        Email(message=_("This should be a valid email address."))
    ])
    displayname = TextField(_('Display name'))
    password = PasswordField(_('Password'), [Required(),
        Length(min=8, message=_("It's probably best if your password is longer than 8 characters."))
    ])
    role = SelectField(_('Role'), choices=[(ROOT, 'Root'),(MANAGER, 'Manager'),(ADMIN, 'Admin')], coerce=int)
    language = SelectField(_('Language'), choices=[('en', _('English')),('fr', _('French'))])
    organisations = QuerySelectField(_('Organisation'), get_label='name',query_factory=get_organisations)
    submit = SubmitField(_('Save'))

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

class AccountFormEdit(Form):
    username = TextField(_('Username'), [Required(),
        Length(min=3, max=20),
        Regexp(r'^[^@:]*$', message=_("Username shouldn't contain '@' or ':'"))
    ])
    email = EmailField(_('Email address'), [
        Length(min=3, max=128),
        Email(message=_("This should be a valid email address."))
    ])
    displayname = TextField(_('Display name'))
    password = PasswordField(_('Password'), [Required(),
        Length(min=8, message=_("It's probably best if your password is longer than 8 characters."))
    ])
    role = SelectField(_('Role'), choices=[(ROOT, 'Root'),(MANAGER, 'Manager'),(ADMIN, 'Admin')], coerce=int)
    submit = SubmitField(_('Save'))

    language = SelectField(_('Language'), choices=[('en', _('English')),('fr', _('French'))])

    organisations = QuerySelectField(_('Organisation'), get_label='name',query_factory=get_organisations)


class SignupForm(Form):
    displayname = TextField(_('Display name'))

    username = TextField(_('Username'), [Required(),
        Length(min=3, max=20),
        Regexp(r'^[^@:]*$', message=_("Username shouldn't contain '@' or ':'"))
    ])
    email = EmailField(_('Email address'), [Required(),
        Length(min=3, max=128),
        Email(message=_("This should be a valid email address."))
    ])
    password = PasswordField(_('Password'), [
        Required(),
        Length(min=8, message=_("It's probably best if your password is longer than 8 characters.")),
        EqualTo('confirm', message=_("Passwords must match."))
    ])
    confirm = PasswordField(_('Confirm password'))
    captcha = RecaptchaField(_('Captcha'))

    agree = BooleanField(_('Agree to the <a href="#license" role="button" class="btn-text" data-toggle="modal">terms and conditions</a>'), [Required()])

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

