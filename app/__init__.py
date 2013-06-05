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

from flask import Flask, render_template
from flask.ext.login import LoginManager
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.principal import Principal, Permission, RoleNeed
from decorators import required_role
from register_plugins import Plugins

app = Flask(__name__)
app.config.from_object('conf')

db = SQLAlchemy(app)

Principal(app)
admin_role = Permission(RoleNeed('admin'))
manager_role = Permission(RoleNeed('manager')).union(admin_role)
user_role = Permission(RoleNeed('user')).union(manager_role)

lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login.login'

from core.server.models import Servers
servers_list = Servers.query.order_by(Servers.name)

plugins_list = ""
plugins = Plugins(app)
plugins.init_plugins()
plugins_list = plugins.register_plugins(app)

from app.core.login.views import login_form
app.register_blueprint(login_form)

from app.core.server.views import servers
app.register_blueprint(servers)

from app.core.profil.views import profil
app.register_blueprint(profil)

from home import home
