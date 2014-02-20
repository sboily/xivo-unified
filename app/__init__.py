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

from flask import Flask, session, g, flash, redirect, url_for, request
from flask.ext.login import current_user, user_logged_in
from flask.ext.principal import identity_loaded
from extensions import db, babel, celery, login_manager, principal, couchdbmanager, mail
from flask.ext.babel import gettext as _
import plugin_manager
import logging

CORE_MODULES = (
    'servers',
    'authentification',
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
    app = Flask(__name__)
    configure_app(app)
    configure_core_modules(app)
    configure_extensions(app)
    configure_hooks(app)
    configure_logging(app)
    configure_error_handlers(app)

    return app

def configure_app(app):
    app.config.from_object('conf')
    celery.config_from_object(app.config)

def configure_core_modules(app):
    for module in CORE_MODULES:
        exec("from app.core.%s.views import %s" %(module, module))
        exec("app.register_blueprint(%s)" % module)

def configure_extensions(app):
    # I18N
    babel.init_app(app)

    # Database
    db.init_app(app)

    # CouchDB
    couchdbmanager.setup(app)
    couchdbmanager.sync(app)

    # Login
    login_manager.init_app(app)
    login_manager.login_view = 'authentification.login'

    # Roles
    principal.init_app(app)

    # Mail
    mail.init_app(app)

    # Plugins list global
    plugin_manager.init_plugin_manager(app.root_path + '/plugins', app)
    plugin_manager.activate_plugins()
    plugin_manager.setup_plugins()

def configure_hooks(app):
    @app.before_request
    def before_request():
        if current_user.is_authenticated():
            if session.get('server_id', None):
                g.server_id = session['server_id']
                g.server = core.servers.views.get_my_server()

            g.servers_list = core.servers.views.get_servers_list()
            g.plugins_list = plugin_manager.get_plugin_list()

    @login_manager.user_loader
    def load_user(id):
        return core.authentification.auth.get_user_by_id(id)

    @user_logged_in.connect_via(app)
    def on_user_logged_in(cur, user):
        print "User : %s is logged ..." % user.displayname

    @identity_loaded.connect_via(app)
    def on_identity_loaded(sender, identity):
        if identity.id:
            current_user.from_identity(identity)

    @babel.localeselector
    def get_locale():
        if hasattr(current_user, 'language'):
            return current_user.language
        else:
            return request.accept_languages.best_match(LANGUAGES.keys())

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
