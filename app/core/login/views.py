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

from flask import render_template, redirect, session, url_for, request, Blueprint, current_app
from flask.ext.login import login_user, logout_user, current_user
from flask.ext.principal import Identity, identity_changed
from forms import LoginForm
from app.models import User
from auth import Auth

login = Blueprint('login', __name__, template_folder='templates/login')

@login.before_request
def is_root_installed():
    if not User.query.filter(User.role == '300').first():
        return redirect(url_for('home.first'))

@login.route("/login", methods=['GET', 'POST'])
def log():
    if current_user.is_authenticated():
        return redirect(url_for('home.homepage'))

    form = LoginForm()
    del form.language
    if form.validate_on_submit():
        user = Auth(form.username.data, form.password.data)
        if user.is_active:
            login_user(user, remember=form.remember_me.data)
            identity_changed.send(current_app._get_current_object(), identity=Identity(user.id))
            return redirect(request.args.get('next') or url_for('home.homepage'))
    return render_template('login.html', form=form)

@login.route("/logout")
def logout():
    for key in ('identity.name', 'identity.auth_type', 'server_id', \
                'organisation_id', 'server', 'user'):
        session.pop(key, None)

    logout_user()
    return redirect(url_for('login.log'))
