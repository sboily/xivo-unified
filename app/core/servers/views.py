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
from app.models import Servers, User, Organisations
from forms import ServersForm
from app.extensions import db
from app.helpers.acl.roles import manager_role, admin_role
from flask.ext.babel import gettext as _

servers = Blueprint('servers', __name__, template_folder='templates/server')

@servers.route('/server')
@login_required
@manager_role.require(403)
def server():
    servers = get_servers_list()
    return render_template('server.html', servers=servers)

@servers.route('/server/add', methods=['GET', 'POST'])
@login_required
@manager_role.require(403)
def server_add():
    form = ServersForm()
    if g.user.role != 300:
        form.organisations.query_factory = lambda: Organisations.query.filter(Organisations.id == g.user_organisation.id).all()
        form.organisations.allow_blank = False

    if form.validate_on_submit():
        server = Servers(form.name.data, form.address.data,
                         form.login.data, form.password.data)

        users = _add_users(form)
        server.users = users
        server.organisation_id = form.organisations.data.id
        server.protocol = form.protocol.data

        db.session.add(server)
        db.session.commit()
        flash(_('Server added'))
        return redirect(url_for("servers.server"))
    return render_template('server_add.html', form=form)

@servers.route('/server/del/<id>')
@login_required
@manager_role.require(403)
def server_del(id):
    if g.user.role == 300:
        server = Servers.query.get_or_404(id)
    else:
        server = Servers.query.join(User.servers).filter(User.id == current_user.id) \
                                                 .filter(Servers.id == id) \
                                                 .order_by(Servers.name).first()
    if server:
        db.session.delete(server)
        db.session.commit()
    return redirect(url_for("servers.server"))

@servers.route('/server/edit/<id>', methods=['GET', 'POST'])
@login_required
@manager_role.require(403)
def server_edit(id):
    if g.user.role == 300:
        server = Servers.query.get_or_404(id)
        form = ServersForm(obj=server)
    else:
        server = Servers.query.join(User.servers).filter(User.organisation_id==g.user_organisation.id) \
                                                 .filter(Servers.id == id) \
                                                 .order_by(Servers.name).first()
        form = ServersForm(obj=server)
        form.users.query_factory = lambda: User.query.filter(Servers.organisation_id == Organisations.id) \
                                                     .filter(Servers.organisation_id == User.organisation_id) \
                                                     .filter(User.organisation_id == g.user.organisation_id) \
                                                     .filter(Servers.id == id) \
                                                     .all()

    form.organisations.allow_blank = False
    if form.validate_on_submit():
        form.populate_obj(server)

        users = _add_users(form)

        server.users = users
        db.session.add(server)
        db.session.commit()
        flash(_('Server edit'))
        return redirect(url_for("servers.server"))
    return render_template('server_edit.html', form=form)

@servers.route('/server/save/<id>')
@login_required
@admin_role.require(403)
def server_save(id):
    if g.user.role == 300:
        server = Servers.query.order_by(Servers.name).first()
    elif g.user.role == 200:
        server = Servers.query.join(User.servers).filter(User.organisation_id == g.user.organisation_id) \
                                                 .order_by(Servers.name)
    else:
        server = Servers.query.join(User.servers).filter(User.id == current_user.id) \
                                                 .filter(Servers.id == id) \
                                                 .order_by(Servers.name).first()
    if server:
        session['server_id'] = id
        session.modified = True
        return redirect(url_for('home.home_server'))

    return redirect(url_for("servers.server"))


@servers.route('/server/disconnect')
@login_required
@admin_role.require(403)
def server_disconnect():
    if session.has_key('server_id') and session['server_id']:
        del session['server_id']
        g.server_id = ""
        g.server = ""
    return redirect(url_for("home.homepage"))

def get_servers_list():
    if g.user.role == 300:
        servers = Servers.query.order_by(Servers.organisation_id)
    elif g.user.role == 200:
        servers = Servers.query.join(User.servers) \
                               .filter(User.organisation_id == g.user.organisation_id) \
                               .order_by(Servers.name)
    else:
        servers = Servers.query.join(User.servers) \
                               .filter(User.id == g.user.id) \
                               .order_by(Servers.name)

    return servers

def get_my_server():
    return Servers.query.get(g.server_id)

def _add_users(form):
    users = []
    auto_add = False
    for choice in form.users.iter_choices():
        if choice[2]:
            user = User.query.filter_by(id=choice[0]).first()
            users.append(user)
        if int(choice[0]) == int(current_user.id) and choice[2] == False:
            if g.user.role != 300:
                auto_add = True

    if auto_add:
        flash(_('Missing your self but added automaticaly !'))
        user = User.query.filter_by(id=current_user.id).first()
        users.append(user)

    return users
