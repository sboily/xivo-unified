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
from models import Organisations, UsersOrganisation
from app.core.login.models import User
from forms import OrganisationsForm
from app import db, manager_role, user_role
from flask.ext.babel import gettext as _

organisations = Blueprint('organisations', __name__, template_folder='templates/organisations')

@organisations.route('/organisations')
@login_required
@manager_role.require(403)
def organisation():
    organisations = _get_organisations()
    return render_template('organisations.html', organisations=organisations)

@organisations.route('/organisation/add', methods=['GET', 'POST'])
@login_required
@manager_role.require(403)
def organisation_add():
    form = OrganisationsForm()
    if form.validate_on_submit():
        organisation = Organisations(form.name.data)
        db.session.add(organisation)
        for choice in form.users.iter_choices():
            if choice[2]:
                user = User.query.filter_by(id=choice[0]).first()
                relation = UsersOrganisation(user=user,organisation=organisation)
                db.session.add(relation)

        if current_user.id not in form.users.iter_choices():
            flash(_('Missing your self but added automaticaly !'))
            user = User.query.filter_by(id=current_user.id).first()
            relation = UsersOrganisation(user=user,organisation=organisation)
            db.session.add(relation)

        db.session.commit()
        flash(_('Server added'))
        return redirect(url_for("organisations.organisation"))
    return render_template('organisation_add.html', form=form)

@organisations.route('/organisation/del/<id>')
@login_required
@manager_role.require(403)
def organisation_del(id):
    organisations = Organisations.query.filter(Organisations.id == UsersOrganisation.organisation_id) \
                           .filter(UsersOrganisation.user_id == current_user.id) \
                           .filter(UsersOrganisation.organisation_id == id).first()
    if organisations is None and g.user.role < 200:
        flash(_('You are not authorized !'))
        return redirect(url_for("organisations.organisation"))
    organisation = Organisations.query.filter_by(id=id).first()
    users_organisation = UsersOrganisation.query.filter_by(organisation_id=id).filter_by(user_id=current_user.id).first()
    db.session.delete(organisation)
    if users_organisation is not None:
        db.session.delete(users_organisation)
    db.session.commit()
    return redirect(url_for("organisations.organisation"))

@organisations.route('/organisation/edit/<id>', methods=['GET', 'POST'])
@login_required
@manager_role.require(403)
def organisation_edit(id):
    organisation = Organisations.query.filter(Organisations.id == UsersOrganisation.organisation_id) \
                          .filter(UsersOrganisation.user_id == current_user.id) \
                          .filter(UsersOrganisation.organisation_id == id).first()
    #users = UsersOrganisation.query.filter_by(organisation_id=id).all()
    form = OrganisationsForm(obj=organisation)
    if form.validate_on_submit():
        form.populate_obj(organisation)
        db.session.add(organisation)
        db.session.commit()
        flash(_('Server edit'))
        return redirect(url_for("organisations.organisation"))
    return render_template('organisation_edit.html', form=form)

@organisations.route('/organisation/save/<id>')
@login_required
@user_role.require(403)
def organisation_save(id):
    organisations = Organisations.query.filter(Organisations.id == UsersOrganisation.organisation_id) \
                           .filter(UsersOrganisation.user_id == current_user.id) \
                           .filter(UsersOrganisation.organisation_id == id).first()
    if organisations is None and g.user.role != 300:
        flash(_('You are not authorized !'))
        return redirect(url_for("organisations.organisation"))
    session['organisation_id'] = id
    session.modified = True
    return redirect(url_for('home.home_organisation'))


def _get_organisations():
    if g.user.role == 300:
        organisations = Organisations.query.order_by(Organisations.name)
    else:
        organisations = Organisations.query.filter(Organisations.id == UsersOrganisation.organisation_id) \
                               .filter(UsersOrganisation.user_id == current_user.id).order_by(Organisations.name)
    return organisations
