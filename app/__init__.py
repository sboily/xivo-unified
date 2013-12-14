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
from app.extensions import db, login_manager, babel, principal, celery
from models import Servers, User, Organisations

import plugin_manager
import os
import logging

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
    celery.config_from_object(app.config)


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

def whoami(id):
    me = User.query.filter(User.id == id).first()
    print me.id

def configure_hooks(app):
    @app.before_request
    def before_request():
        if current_user.is_authenticated():
            whoami(current_user.id)

            if g.user.organisation_id:
                g.user_organisation = Organisations.query.get(g.user.organisation_id)

            if "server_id" in session:
                g.server_id = session['server_id']
                g.server = Servers.query.get(session['server_id'])

            g.servers_list = get_servers_list(g.user.role)
            g.plugins_list = plugin_manager.get_plugin_list()

    @identity_loaded.connect_via(app)
    def on_identity_loaded(sender, identity):
        if identity.id:
            g.user = User.query.from_identity(identity)

    @babel.localeselector
    def get_locale():
        if hasattr(g, 'user') and hasattr(g.user, 'language'):
            return g.user.language
        else:
            return request.accept_languages.best_match(LANGUAGES.keys())

def get_servers_list(role):
    if role == 300:
        servers = Servers.query.order_by(Servers.name)
    elif role == 200:
        servers = Servers.query.join(User.servers).filter(User.organisation_id == g.user.organisation_id).order_by(Servers.name)
    else:
        servers = Servers.query.join(User.servers).filter(User.id == g.user.id).order_by(Servers.name)

    return servers

def configure_error_handlers(app):
    @app.errorhandler(403)
    def page_not_authorized(e):
        flash(_('Sorry you are not authorized !'))
        return redirect(url_for('home.homepage'))

    @app.errorhandler(404)
    def page_not_found(e):
        flash('Sorry this page is not found !')
        return redirect(url_for('home.homepage'))

def configure_logging(app):
    app.logger.setLevel(logging.INFO)

# Configure roles
root_role = Permission(RoleNeed('root'))
manager_role = Permission(RoleNeed('manager')).union(root_role)
admin_role = Permission(RoleNeed('admin')).union(manager_role)
