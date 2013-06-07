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


from flask.ext.wtf import Form, TextField, BooleanField, PasswordField, ValidationError, SelectField, RecaptchaField, html5, fields, validators, SubmitField, Required

class AccountForm(Form):
    username = TextField('Username', [Required(),
        validators.Length(min=3, max=20),
        validators.Regexp(r'^[^@:]*$', message="Username shouldn't contain '@' or ':'")
    ])
    email = html5.EmailField('Email address', [
        validators.Length(min=3, max=128),
        validators.Email(message="This should be a valid email address.")
    ])
    displayname = TextField('Display name')
    password = PasswordField('Password', [Required(),
        validators.Length(min=8, message="It's probably best if your password is longer than 8 characters.")
    ])
    role = SelectField('Role', choices=[('300', 'Admin'),('200', 'Manager'),('100', 'User')])

class SignupForm(Form):
    displayname = TextField('Display name')

    username = TextField('Username', [Required(),
        validators.Length(min=3, max=20),
        validators.Regexp(r'^[^@:]*$', message="Username shouldn't contain '@' or ':'")
    ])
    email = html5.EmailField('Email address', [
        validators.Length(min=3, max=128),
        validators.Email(message="This should be a valid email address.")
    ])
    password = PasswordField('Password', [
        Required(),
        validators.Length(min=8, message="It's probably best if your password is longer than 8 characters."),
        validators.EqualTo('confirm', message="Passwords must match.")
    ])
    confirm = PasswordField('Confirm password')
    captcha = RecaptchaField('Captcha')

    agree = BooleanField('I agree with the Terms and Conditions')

    submit = SubmitField('Signup')
