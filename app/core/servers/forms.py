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


from flask.ext.wtf import TextField, BooleanField, PasswordField, ValidationError, QuerySelectField, SubmitField, QuerySelectMultipleField, SelectMultipleField
from flask.ext.wtf import Required, IPAddress, Regexp, validators, SelectField
from wtforms import widgets
from app.models import User, Servers, Organisations
from app.utils import Form
from flask.ext.babel import lazy_gettext as _
from flask import g

def get_servers_list():
    if g.user.role == 300:
        return User.query.order_by(User.displayname)
    else:
        return User.query.filter(User.organisation_id==g.user_organisation.id) \
                         .order_by(User.displayname)

class ServersForm(Form):
    name = TextField(_('Name'), [Required(),
        validators.Length(min=3, max=30),
        validators.Regexp(r'^[^@:]*$', message=_("Name shouldn't contain '@' or ':'"))
    ])

    address = TextField(_('Address'), [Required(), IPAddress()])
    login = TextField(_('Login'))
    password = PasswordField(_('Password'), widget=widgets.PasswordInput(hide_value=False))

    protocol = SelectField(_('Protocol'), choices=[('1.0', 'V1.0'),('1.1', 'V1.1')])

    organisations = QuerySelectField(_('Organisations'), [Required()], get_label='name', \
                                       query_factory=lambda: Organisations.query, \
                                       allow_blank=True, blank_text=_('Please choose an organisation ...'))
    users = QuerySelectMultipleField(_('Users'), get_label='displayname', query_factory=get_servers_list)

    submit = SubmitField(_('Submit'))

    #def validate_users(self, field):
    #    print len(list(field.iter_choices()))
    #    for choice in field.iter_choices():
    #        print choice

        #raise ValidationError(_('Missing your self !'))

