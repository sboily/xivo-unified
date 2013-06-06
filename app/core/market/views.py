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

from flask import render_template, Blueprint, flash, redirect, url_for, g, flash
from flask.ext.login import login_required
from app import db, admin_role, app
import json
import urllib2
import shutil
import os
import tarfile

market = Blueprint('market', __name__, template_folder='templates/market')

@market.route('/market')
@login_required
@admin_role.require(403)
def themarket():
    url = "http://market.xivo.fr/market.json"
    json_read = urllib2.urlopen(url).read()
    modules = json.loads(json_read)
    return render_template('market.html', modules=modules)

@market.route('/market/del/<module>')
@login_required
@admin_role.require(403)
def market_del(module):
    print "Removing module %s" % module
    src = os.path.join(app.config['BASEDIR'], 'app/plugins/%s' % module)
    shutil.rmtree(src)
    flash('Module %s has been removed !' % module)
    return redirect(url_for("reload_app"))

@market.route('/market/get/<module>')
@login_required
@admin_role.require(403)
def market_get(module):
    print "Installing module %s" % module
    dst = os.path.join(app.config['BASEDIR'], 'app/plugins/')
    src = "/tmp/"
    url = "http://market.xivo.fr/%s.tgz" % module
    mod = urllib2.urlopen(url)
    mod_file = open(src + url.split('/')[-1], 'w')
    mod_file.write(mod.read())
    mod_file.close()
    mod.close()
    tar = tarfile.open(src + module + ".tgz")
    tar.extractall(path=dst)
    tar.close()
    flash('Module %s has been installed !' % module)
    return redirect(url_for("reload_app"))
