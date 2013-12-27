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

from flask import render_template, Blueprint, flash, redirect, url_for, g, flash, current_app
from flask.ext.login import login_required
from app.extensions import db
from app.helpers.acl.roles import user_role
from flask.ext.babel import gettext as _
from app.models import Plugins
from app import plugin_manager
import json
import urllib2

market = Blueprint('market', __name__, template_folder='templates/market')

@market.route('/market')
@login_required
@user_role.require(403)
def themarket():
    modules = _get_modules()
    return render_template('market.html', modules=modules)

@market.route('/market/del/<module>')
@login_required
@user_role.require(403)
def market_del(module):
    _remove_module(module)
    flash(_('Module %s has been removed !' % module))
    return redirect(url_for('market.themarket'))

@market.route('/market/get/<module>')
@login_required
@user_role.require(403)
def market_get(module):
    _install_module(module)
    flash(_('Module %s has been installed !' % module))
    return redirect(url_for('home.reload_app'))

def _get_modules():
    url = "http://market.xivo.fr/market.json"
    json_read = urllib2.urlopen(url).read()
    modules = json.loads(json_read)

    for module in modules:
        module['installed'] = _is_module_installed(module)
        module[u'version_installed'] = _module_version_installed(module)

    return modules

def _is_module_installed(module):
    available_modules = [m['module'] for m in plugin_manager.get_plugin_list()]
    return module['name'] in available_modules

def _module_version_installed(module):
    for m in plugin_manager.get_plugin_list():
        if module['name'] == m['module']:
            return m['version']
    return module['informations']['version']

def _remove_module(module):
    print "Removing module %s" % module
    plugin_manager.remove_plugin(module)

def _install_module(module):
    print "Installing module %s" % module
    plugin_manager.install_plugin(module)
