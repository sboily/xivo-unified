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

from flask import render_template, Blueprint
from flask.ext.login import login_required
from app import db, plugins_list, servers_list
from app.core.login.models import User, Role

profil = Blueprint('profil', __name__, template_folder='templates/profil')


@profil.route('/myprofil/<id>')
@login_required
def myprofil(id):
    return render_template('profil.html', servers_list=servers_list, plugins_list=plugins_list)


@profil.route('/accounts')
@login_required
def accounts():
    users = User.query.all()
    return render_template('accounts.html', servers_list=servers_list, plugins_list=plugins_list, users=users)
