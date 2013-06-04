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

from flask import render_template, Blueprint, session
from flask.ext.login import login_required
from app import db, servers_list, plugins_list
from app.server.models import Servers
from restclient import GET, POST, PUT, DELETE
import json

users = Blueprint('users', __name__, template_folder='templates/users')

@users.route('/users')
@login_required
def user():
    id = session['server_id']
    server = Servers.query.get_or_404(id)
    r = GET("https://%s:50051/1.0/users/" % server.address, 
             headers={'Content-Type': 'application/json'}, 
             httplib_params={'disable_ssl_certificate_validation' : True})
    d = json.loads(r)
    return render_template('users.html', servers_list=servers_list, plugins_list=plugins_list, server=server, users=d['items'])
