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

from flask import render_template, Blueprint, current_app, g, redirect, url_for, flash, jsonify
from flask.ext.login import login_required
from app import db
from app.core.organisations.forms import OrganisationsForm
from app.models import User, Organisations
from flask.ext.babel import gettext as _
import os

home = Blueprint('home', __name__, template_folder='templates/login')

@home.route('/')
@login_required
def homepage():
    if g.wizard:
        return redirect(url_for('home.wizard'))
    return render_template('base.html')

@home.route('/reload')
@login_required
def reload_app():
    os.utime(current_app.config['BASEDIR'] + '/app/__init__.py',None)
    return render_template('reload.html')

@home.route('/home')
@login_required
def home_server():
    return render_template('home_server.html')

@home.route('/wizard', methods=['GET', 'POST'])
@login_required
def wizard():
    form = OrganisationsForm()
    del form.users
    if form.validate_on_submit():
        organisation = Organisations(form.name.data)

        user = User.query.get_or_404(g.user.id)

        organisation.users = [user]
        db.session.add(organisation)
        db.session.commit()
        flash(_('Organisation added'))
        return redirect(url_for("home.homepage"))
    return render_template('wizard.html', form=form)
