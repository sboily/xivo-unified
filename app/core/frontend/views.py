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

from flask import render_template, Blueprint, redirect
from flask.ext.login import current_user

frontend = Blueprint('frontend', __name__, template_folder='templates/frontend',
                      static_folder='static', static_url_path='/%s' % __name__)

@frontend.route('/')
def homepage():
    if current_user.is_authenticated():
        return redirect('home.homepage')
    return render_template('index.html', is_anonymous_content=1)