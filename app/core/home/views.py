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

from flask import render_template, Blueprint, current_app
from flask.ext.login import login_required
from app import create_app as app
import os

home = Blueprint('home', __name__, template_folder='templates/login')

@home.route('/')
@login_required
def homepage():
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

