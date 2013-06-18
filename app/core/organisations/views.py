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

from flask import render_template, Blueprint, request, flash, redirect, url_for, session, g, jsonify
from flask.ext.login import login_required, current_user
from app.models import Organisations, User
from forms import OrganisationsForm
from app import db, root_role, manager_role, admin_role
from flask.ext.babel import gettext as _

organisations = Blueprint('organisations', __name__, template_folder='templates/organisations')

@organisations.route('/organisations')
@login_required
@root_role.require(403)
def organisation():
    organisations = _get_organisations()
    return render_template('organisations.html', organisations=organisations)

@organisations.route('/organisation/add', methods=['GET', 'POST'])
@login_required
@root_role.require(403)
def organisation_add():
    form = OrganisationsForm()
    if form.validate_on_submit():
        organisation = Organisations(form.name.data)

        users = _add_users(form)

        organisation.users = users
        db.session.add(organisation)
        db.session.commit()
        flash(_('Organisation added'))
        return redirect(url_for("organisations.organisation"))
    return render_template('organisation_add.html', form=form)

@organisations.route('/organisation/del/<id>')
@login_required
@root_role.require(403)
def organisation_del(id):
    organisations = Organisations.query \
                                 .filter(Organisations.id == id) \
                                 .first()

    if organisations:
        db.session.delete(organisations)
        db.session.commit()
        flash(_('Organisation deleted'))
    return redirect(url_for("organisations.organisation"))

@organisations.route('/organisation/edit/<id>', methods=['GET', 'POST'])
@login_required
@root_role.require(403)
def organisation_edit(id):
    organisation = Organisations.query \
                                .join(User.organisations) \
                                .filter(Organisations.id == id) \
                                .first()
 
    form = OrganisationsForm(obj=organisation)
    if form.validate_on_submit():
        form.populate_obj(organisation)

        users = _add_users(form)

        organisation.users = users
        db.session.add(organisation)
        db.session.commit()
        flash(_('Organisation edit'))
        return redirect(url_for("organisations.organisation"))
    return render_template('organisation_edit.html', form=form)

@organisations.route('/organisation/accounts/<id>')
@login_required
@root_role.require(403)
def organisation_accounts(id):
    users = []
    lists = User.query.filter(Organisations.id == id) \
                      .filter(User.organisation_id == Organisations.id) \
                      .order_by('displayname')

    for user in lists:
        users.append({'id': user.id, 'displayname': user.displayname})
    return jsonify(accounts=users)


def _get_organisations():
        return Organisations.query.order_by(Organisations.name)

def _add_users(form):
    users = []
    for choice in form.users.iter_choices():
        if choice[2]:
            user = User.query.filter_by(id=choice[0]).first()
            users.append(user)

    return users

