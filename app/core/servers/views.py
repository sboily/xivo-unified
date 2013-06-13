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

from flask import render_template, Blueprint, request, flash, redirect, url_for, session, g
from flask.ext.login import login_required, current_user
from app.models import Servers, UsersServer, User
from forms import ServersForm
from app import db, manager_role, admin_role
from flask.ext.babel import gettext as _

servers = Blueprint('servers', __name__, template_folder='templates/server')

@servers.route('/server')
@login_required
@manager_role.require(403)
def server():
    servers = _get_servers()
    return render_template('server.html', servers=servers)

@servers.route('/server/add', methods=['GET', 'POST'])
@login_required
@manager_role.require(403)
def server_add():
    auto_add = False
    form = ServersForm()
    if form.validate_on_submit():
        server = Servers(form.name.data, form.address.data,
                         form.login.data, form.password.data)
        db.session.add(server)
        for choice in form.users.iter_choices():
            print choice[0], current_user.id, choice[2]
            if choice[2]:
                user = User.query.filter_by(id=choice[0]).first()
                relation = UsersServer(user=user,server=server)
                db.session.add(relation)
            if int(choice[0]) == int(current_user.id) and choice[2] == False:
                auto_add = True

        if auto_add:
            flash(_('Missing your self but added automaticaly !'))
            user = User.query.filter_by(id=current_user.id).first()
            relation = UsersServer(user=user,server=server)
            db.session.add(relation)

        db.session.commit()
        flash(_('Server added'))
        return redirect(url_for("servers.server"))
    return render_template('server_add.html', form=form)

@servers.route('/server/del/<id>')
@login_required
@manager_role.require(403)
def server_del(id):
    servers = Servers.query.filter(Servers.id == UsersServer.server_id) \
                           .filter(UsersServer.user_id == current_user.id) \
                           .filter(UsersServer.server_id == id).first()
    if servers is None and g.user.role < 200:
        flash(_('You are not authorized !'))
        return redirect(url_for("servers.server"))
    server = Servers.query.filter_by(id=id).first()
    users_server = UsersServer.query.filter_by(server_id=id).filter_by(user_id=current_user.id).first()
    db.session.delete(server)
    if users_server is not None:
        db.session.delete(users_server)
    db.session.commit()
    return redirect(url_for("servers.server"))

@servers.route('/server/edit/<id>', methods=['GET', 'POST'])
@login_required
@manager_role.require(403)
def server_edit(id):
    server = Servers.query.filter(Servers.id == UsersServer.server_id) \
                          .filter(UsersServer.user_id == current_user.id) \
                          .filter(UsersServer.server_id == id).first()
    form = ServersForm(obj=server)
    if form.validate_on_submit():
        form.populate_obj(server)
        db.session.add(server)
        db.session.commit()
        flash(_('Server edit'))
        return redirect(url_for("servers.server"))
    return render_template('server_edit.html', form=form)

@servers.route('/server/save/<id>')
@login_required
@admin_role.require(403)
def server_save(id):
    servers = Servers.query.filter(Servers.id == UsersServer.server_id) \
                           .filter(UsersServer.user_id == current_user.id) \
                           .filter(UsersServer.server_id == id).first()
    if servers is None and g.user.role != 300:
        flash(_('You are not authorized !'))
        return redirect(url_for("servers.server"))
    session['server_id'] = id
    session.modified = True
    return redirect(url_for('home.home_server'))


def _get_servers():
    if g.user.role == 300:
        servers = Servers.query.order_by(Servers.name)
    else:
        servers = Servers.query.filter(Servers.id == UsersServer.server_id) \
                               .filter(UsersServer.user_id == current_user.id).order_by(Servers.name)
    return servers
