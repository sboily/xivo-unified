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

from flask import render_template, g, session, flash, redirect, url_for
from decorators import required_role
from flask.ext.login import current_user
from flask.ext.principal import identity_loaded
from app import app, servers_list, plugins_list
from core.server.models import Servers
from core.login.models import User
from flask.ext.login import login_required
import sys, os, time
from register_plugins import Plugins


@app.before_request
def before_request():
    if current_user.is_authenticated():
        g.plugins_list = plugins_list
        g.servers_list = servers_list
        if session.has_key('server_id') and session['server_id']:
            g.server_id = session['server_id']
            g.server = Servers.query.get_or_404(session['server_id'])
    else:
        print 'User not authentified !'

@identity_loaded.connect_via(app)
def on_identity_loaded(sender, identity):
    g.user = User.query.from_identity(identity)

@app.route('/')
@login_required
def home():
    return render_template('base.html')

@app.route('/reload')
def reload_app():
    os.utime(app.config['BASEDIR'] + '/app/__init__.py',None)
    return render_template('reload.html')

@app.route('/home')
@login_required
def home_server():
    return render_template('home_server.html')

@app.errorhandler(403)
def page_not_found(e):
    flash('Sorry you are not authorized !')
    return redirect(url_for("home"))
