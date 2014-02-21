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

from flask import render_template, Blueprint, current_app, g, redirect, url_for, flash, request
from flask.ext.login import login_required, current_user
from app.core.organisations.forms import OrganisationsForm
from app.core.profil.forms import AccountForm
from app.models import User, Organisations
from flask.ext.babel import gettext as _
from app import db
import os

home = Blueprint('home', __name__, template_folder='templates/home')

@home.before_app_first_request
def initdb():
    db.create_all()
    db.session.commit()

@home.route('/backend')
@login_required
def homepage():
    if not current_user.organisation_id \
        or not current_user.organisation_domain:
        return redirect(url_for('home.wizard'))
    return render_template('home.html')

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
    if current_user.organisation_name:
        organisation = Organisations.query.filter_by(id=current_user.organisation_id).first()
        form = OrganisationsForm(obj=organisation)
        form.name.data = current_user.organisation_name
    else:
        form = OrganisationsForm()
    if form.validate_on_submit():
        if current_user.organisation_name:
            form.populate_obj(organisation)
        else:
            organisation = Organisations(form.name.data)
            organisation.domain = form.domain.data
            user = User.query.get_or_404(current_user.id)
            organisation.users = [user]
        db.session.add(organisation)
        db.session.commit()
        flash(_('Organisation added'))
        return redirect(url_for("home.homepage"))
    return render_template('wizard.html', form=form)

@home.route('/first', methods=['GET', 'POST'])
def first():
    if not current_user.is_anonymous:
        return redirect(url_for("home.homepage"))

    form = AccountForm()
    del form.organisations
    del form.role
    del form.language
    if form.validate_on_submit():
        account = User(form.username.data, form.password.data,
                       form.email.data, form.displayname.data, '300')
        db.session.add(account)
        db.session.commit()
        flash(_('Account added'))
        return redirect(url_for("home.homepage"))
    return render_template('first.html', form=form)
