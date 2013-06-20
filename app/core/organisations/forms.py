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


from flask.ext.wtf import TextField, BooleanField, PasswordField, ValidationError, QuerySelectField, SubmitField, QuerySelectMultipleField, TextAreaField
from flask.ext.wtf import Required, Regexp, validators
from flask.ext.login import current_user
from flask.ext.babel import lazy_gettext as _
from app.utils import Form
from app.models import User
from wtforms import widgets

class OrganisationsForm(Form):
    name = TextField(_('Name'), [Required(),
        validators.Length(min=3, max=30),
        validators.Regexp(r'^[^@:]*$', message=_("Name shouldn't contain '@' or ':'"))
    ])

    description = TextAreaField(_('Description'))

    users = QuerySelectMultipleField(_('Users'), get_label='displayname',query_factory=lambda: User.query.order_by(User.displayname))

    submit = SubmitField(_('Submit'))


    def validate_users(self, field):
        miss_me = False
        for choice in field.iter_choices():
            if int(choice[0]) == int(current_user.id) and choice[2] == False:
                miss_me = True

        if miss_me:
            raise ValidationError(_('Missing your self !'))
