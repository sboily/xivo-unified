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

from wtforms.fields import TextField, SubmitField, TextAreaField
from wtforms.validators import Required, Regexp, Length
from flask.ext.babel import lazy_gettext as _
from app.utils import Form

class OrganisationsForm(Form):
    name = TextField(_('Name'), [Required(),
        Length(min=3, max=30),
        Regexp(r'^[^@:]*$', message=_("Name shouldn't contain '@' or ':'"))
    ])

    description = TextAreaField(_('Description'))
    submit = SubmitField(_('Submit'))
