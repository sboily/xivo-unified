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

from flask import Flask, render_template
from flask.ext.login import LoginManager, login_required
from flask.ext.sqlalchemy import SQLAlchemy
from decorators import required_role
from register_plugins import register_plugins

app = Flask(__name__)
app.config.from_object('conf')

db = SQLAlchemy(app)

lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login.login'

try:
    plugins_menu = []
    for plugin in register_plugins(app):
        exec("from app.plugins.%s.views import %s" %(plugin, plugin))
        exec("app.register_blueprint(%s)" % plugin)
        plugins_menu.append(plugin)
except ImportError, e:
    print "Can't register plugin : %s" % e

from app.login.views import login_form
app.register_blueprint(login_form)

from app.server.views import servers
app.register_blueprint(servers)


@app.route('/')
@required_role('admin')
def home():
    return render_template('base.html')

