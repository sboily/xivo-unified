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

from flask import Flask, render_template, session, g, current_app, flash, redirect, url_for, request
from flask.ext.login import LoginManager, current_user
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.principal import Principal, Permission, RoleNeed, identity_loaded, AnonymousIdentity, identity_changed
from app.extensions import db, login_manager, babel, principal
from models import Servers, UsersServer, User

import plugin_manager
import os


CORE_MODULES = (
    'servers',
    'login',
    'market',
    'profil',
    'home',
    'organisations',
)

LANGUAGES = {
    'en': 'English',
    'fr': 'French'
}


def create_app():
    core_modules = CORE_MODULES

    app = Flask(__name__)
    configure_app(app)
    configure_core_modules(app, core_modules)
    configure_extensions(app)
    configure_hooks(app)
    configure_logging(app)
    configure_error_handlers(app)

    return app


def configure_app(app):
    app.config.from_object('conf')


def configure_core_modules(app, core_modules):
    for module in core_modules:
        exec("from app.core.%s.views import %s" %(module, module))
        exec("app.register_blueprint(%s)" % module)


def configure_extensions(app):
    # I18N
    babel.init_app(app)

    # Database
    db.init_app(app)

    # Roles
    principal.init_app(app)

    # Authentification
    login_manager.init_app(app)
    login_manager.login_view = 'login.log'

    @login_manager.user_loader
    def load_user(userid):
        return User.query.filter_by(id=userid).first()

    # Plugins list global
    path = os.path.join(app.config['BASEDIR'], 'app/plugins')
    plugin_manager.init_plugin_manager(path, app)
    plugin_manager.activate_plugins()
    plugin_manager.setup_plugins()


def configure_hooks(app):
    @app.before_request
    def before_request():
        pass

    @identity_loaded.connect_via(app)
    def on_identity_loaded(sender, identity):
        g.plugins_list = _get_plugins_info()
        g.user = ""

        if identity.id:
            g.user = User.query.from_identity(identity)

            if g.user.role == 300:
                g.servers_list = Servers.query.order_by(Servers.name)
            else:
                g.servers_list = Servers.query.filter(Servers.id == UsersServer.server_id) \
                                              .filter(UsersServer.user_id == g.user.id).order_by(Servers.name)

        if session.has_key('server_id') and session['server_id']:
            g.server_id = session['server_id']
            g.server = Servers.query.get(session['server_id'])
            if g.server is None:
                del session['server_id']
                g.server_id = ""
                g.server = ""


    @babel.localeselector
    def get_locale():
        return request.accept_languages.best_match(LANGUAGES.keys())

def configure_error_handlers(app):
    @app.errorhandler(403)
    def page_not_found(e):
        flash('Sorry you are not authorized !')
        return redirect(url_for('home.homepage'))

def configure_logging(app):
    if app.debug or app.testing:
        return

    import logging
    app.logger.setLevel(logging.INFO)


def _get_plugins_info():
    return plugin_manager.get_plugin_list()

# Configure roles
root_role = Permission(RoleNeed('root'))
manager_role = Permission(RoleNeed('manager')).union(root_role)
admin_role = Permission(RoleNeed('admin')).union(manager_role)
