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

from flask import render_template, Blueprint, flash, redirect, url_for, request, g, current_app
from werkzeug.security import generate_password_hash
from flask.ext.login import login_required, current_user
from app.extensions import db
from app.helpers.acl.roles import root_role, manager_role, admin_role, user_role
from app.models import User
from forms import AccountForm, AccountFormEdit, SignupForm
from flask.ext.babel import gettext as _
from flask.ext.gravatar import Gravatar

profil = Blueprint('profil', __name__, template_folder='templates/profil')


@profil.route('/myprofil', methods=['GET', 'POST'])
@login_required
@user_role.require(403)
def myprofil():
    if current_user.is_user:
        account = current_user
    else:
        account = User.query.filter_by(id=current_user.id).first()
    gravatar = Gravatar(current_app,
                    size=140,
                    rating='g',
                    default='retro',
                    force_default=False,
                    use_ssl=False,
                    base_url=None)
    form = AccountFormEdit(obj=account)
    if request.method == 'POST':
        form.username.data = User.query.get_or_404(current_user.id).username
        if not form.password.data and account.password:
            del form.password
        elif form.password.data:
            form.password.data = generate_password_hash(form.password.data)
    if form.validate_on_submit():
        form.populate_obj(account)
        db.session.add(account)
        db.session.commit()
        flash(_('Profil edit'))
        return redirect(url_for("profil.myprofil"))
    else:
        if request.method == 'POST':
            flash(_('Error to save the form !'))
            return redirect(url_for("profil.myprofil"))
    return render_template('profil.html', form=form, account=account)

@profil.route('/accounts')
@login_required
@manager_role.require(403)
def accounts():
    if current_user.is_root:
        users = User.query.all()
    else:
        users = User.query.filter(User.organisation_id == current_user.organisation_id) \
                          .filter(User.role <= current_user.MANAGER) \
                          .all()
    return render_template('accounts.html', users=users)

@profil.route('/account/add', methods=['GET', 'POST'])
@login_required
@manager_role.require(403)
def account_add():
    form = AccountForm()
    if current_user.is_manager:
        form.role.choices = [(current_user.MANAGER, 'Manager'),(current_user.ADMIN, 'Admin')]
    if form.validate_on_submit():
        account = User(form.username.data, form.password.data,
                    form.email.data, form.displayname.data, form.role.data)
        account.language = form.language.data
        account.organisations = form.organisations.data
        db.session.add(account)
        db.session.commit()
        flash(_('Account added'))
        return redirect(url_for("profil.accounts"))
    return render_template('account_add.html', form=form)

@profil.route('/account/del/<id>')
@login_required
@manager_role.require(403)
def account_del(id):
    if current_user.is_root:
        account = User.query.filter_by(id=id).first()
    else:
        account = User.query.filter(User.organisation_id == current_user.organisation_id) \
                            .filter_by(id=id) \
                            .first()
    if account:
        db.session.delete(account)
        db.session.commit()
        flash(_('Account delete'))
    else:
        flash(_('Sorry you are not authorized !'))
    return redirect(url_for("profil.accounts"))

@profil.route('/account/edit/<id>', methods=['GET', 'POST'])
@login_required
@manager_role.require(403)
def account_edit(id):
    if current_user.is_root:
        account = User.query.get_or_404(id)
    else:
        account = User.query.filter(User.organisation_id == current_user.organisation_id) \
                            .filter(User.role <= current_user.MANAGER) \
                            .filter_by(id=id) \
                            .first()
    form = AccountFormEdit(obj=account)
    if current_user.is_manager:
        form.role.choices = [(current_user.MANAGER, 'Manager'),(current_user.ADMIN, 'Admin')]
    if request.method == 'POST':
        form.username.data = User.query.get_or_404(id).username
        if not form.password.data and account.password:
            del form.password
        elif form.password.data:
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
        return redirect(url_for('authentification.login'))
    return render_template('signup.html', form=form)
