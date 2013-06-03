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

from flask import render_template, Blueprint, request, flash, redirect, url_for
from flask.ext.login import login_required
from models import Servers
from forms import ServersForm
from app import db

servers = Blueprint('servers', __name__, template_folder='templates/server')

@servers.route('/server')
@login_required
def server():
    servers = Servers.query.order_by(Servers.name)
    return render_template('server.html', servers=servers)

@servers.route('/server/add', methods=['GET', 'POST'])
@login_required
def server_add():
    serverform = ServersForm()
    if request.method == 'POST' and serverform.validate_on_submit():
        server = Servers(serverform.name.data, serverform.address.data,
                           serverform.login.data, serverform.password.data)
        db.session.add(server)
        db.session.commit()
        flash('Server added')
        return redirect(url_for("servers.server"))
    return render_template('server_add.html', serverform=serverform)

@servers.route('/server/del/<id>')
@login_required
def server_del(id):
    server = Servers.query.filter_by(id=id).first()
    db.session.delete(server)
    db.session.commit()
    return redirect(url_for("servers.server"))

@servers.route('/server/edit/<id>', methods=['GET', 'POST'])
@login_required
def server_edit(id):
    server = Servers.query.get_or_404(id)
    serverform = ServersForm(obj=server)
    if serverform.validate_on_submit():
        serverform.populate_obj(server)
        db.session.add(server)
        db.session.commit()
        flash('Server edit')
        return redirect(url_for("servers.server"))
    return render_template('server_edit.html', serverform=serverform)
