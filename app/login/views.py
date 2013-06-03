# -*- coding: utf-8 -*-

# Copyright (C) 2013 Avencall
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>

from flask import render_template, flash, redirect, session, url_for, request, g, Blueprint
from flask.ext.login import login_user, logout_user, current_user, login_required
from app import app, lm
from forms import LoginForm
from models import User

login_form = Blueprint('login', __name__, template_folder='templates/login')

@lm.user_loader
def load_user(userid):
    return User.query.filter_by(id=userid).first()

@login_form.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated():
        return redirect(url_for('home'))
    loginform = LoginForm()
    if loginform.validate_on_submit():
        user = User.query.filter_by(email=loginform.login.data).first()
        if user and user.check_password(loginform.password.data):
            login_user(user, remember=loginform.remember_me.data)
            return redirect(request.args.get("next") or url_for("home"))
    return render_template('login.html', title='Sign In', loginform=loginform)

@login_form.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("home"))
