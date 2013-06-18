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

from flask import render_template, Blueprint, flash, redirect, url_for, request
from werkzeug.security import generate_password_hash
from flask.ext.login import login_required, current_user
from app import db, root_role, admin_role
from app.models import User
from forms import AccountForm, SignupForm
from flask.ext.babel import gettext as _

profil = Blueprint('profil', __name__, template_folder='templates/profil')


@profil.route('/myprofil', methods=['GET', 'POST'])
@login_required
@admin_role.require(403)
def myprofil():
    account = User.query.get_or_404(current_user.id)
    form = AccountForm(obj=account)
    if form.validate_on_submit():
        form.populate_obj(account)
        db.session.add(account)
        db.session.commit()
        flash(_('Profil edit'))
        return redirect(url_for("profil.myprofil"))
    return render_template('profil.html', form=form)

@profil.route('/accounts')
@login_required
@root_role.require(403)
def accounts():
    users = User.query.all()
    return render_template('accounts.html', users=users)

@profil.route('/account/add', methods=['GET', 'POST'])
@login_required
@root_role.require(403)
def account_add():
    form = AccountForm()
    if form.validate_on_submit():
        account = User(form.username.data, form.password.data,
                    form.email.data, form.displayname.data, form.role.data)
        account.organisations = form.organisations.data
        db.session.add(account)
        db.session.commit()
        flash(_('Account added'))
        return redirect(url_for("profil.accounts"))
    return render_template('account_add.html', form=form)

@profil.route('/account/del/<id>')
@login_required
@root_role.require(403)
def account_del(id):
    account = User.query.filter_by(id=id).first()
    db.session.delete(account)
    db.session.commit()
    flash(_('Account delete'))
    return redirect(url_for("profil.accounts"))

@profil.route('/account/edit/<id>', methods=['GET', 'POST'])
@login_required
@root_role.require(403)
def account_edit(id):
    account = User.query.get_or_404(id)
    form = AccountForm(obj=account)
    if request.method == 'POST':
        form.username.data = User.query.get_or_404(id).username
        form.password.data = generate_password_hash(form.password.data)
    if form.validate_on_submit():
        form.populate_obj(account)
        db.session.add(account)
        db.session.commit()
        flash(_('Account edit'))
        return redirect(url_for("profil.accounts"))
    return render_template('account_edit.html', form=form)

@profil.route('/signup', methods=['GET', 'POST'])
def signup():
    default_role = 200
    form = SignupForm()
    if form.validate_on_submit():
        account = User(form.username.data, form.password.data,
                    form.email.data, form.displayname.data, default_role)
        db.session.add(account)
        db.session.commit()
        flash(_('Account added'))
        return redirect(url_for('login.log'))
    return render_template('signup.html', form=form)
