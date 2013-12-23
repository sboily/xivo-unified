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

from flask import render_template, redirect, session, url_for, request, Blueprint, current_app, flash
from flask.ext.login import login_user, logout_user, current_user, login_required
from flask.ext.principal import Identity, identity_changed
from flask.ext.babel import lazy_gettext as _
from app.helpers.acl.roles import root_role
from forms import LoginForm, AuthServerLdapForm
from app.extensions import db
from app.models import User, AuthServerLdap
from auth import Auth

authentification = Blueprint('authentification', __name__, template_folder='templates/authentification')

@authentification.before_request
def is_root_installed():
    if not User.query.filter(User.role == '300').first():
        return redirect(url_for('home.first'))

@authentification.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated():
        return redirect(url_for('home.homepage'))

    form = LoginForm()
    del form.language
    if form.validate_on_submit():
        user = Auth(form.username.data, form.password.data)
        if user.is_active():
            login_user(user, remember=form.remember_me.data)
            identity_changed.send(current_app._get_current_object(), identity=Identity(user.id))
            return redirect(request.args.get('next') or url_for('home.homepage'))
        else:
            flash(_('Login error, please try again !'))
    return render_template('login.html', form=form)

@authentification.route("/logout")
def logout():
    for key in ('identity.name', 'identity.auth_type', 'server_id', \
                'organisation_id', 'server', 'user'):
        session.pop(key, None)

    logout_user()
    return redirect(url_for('authentification.login'))

@authentification.route("/authentification/server/configure", methods=['GET', 'POST'])
@login_required
@root_role.require(403)
def auth_configure():
    server = AuthServerLdap.query.first()
    form = AuthServerLdapForm(obj=server)
    if form.validate_on_submit():
        if server:
            form.populate_obj(server)
        else:
            server = AuthServerLdap(form.host.data)
            server.basedn = form.basedn.data
            server.searchfilter = form.searchfilter.data
            server.active = form.active.data
        db.session.add(server)
        db.session.commit()
        flash(_('Server LDAP edited'))
    return render_template('authentification_configuration.html', form=form)
