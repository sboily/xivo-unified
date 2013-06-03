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

import os

def register_plugins(app):
    plugins_directory = os.path.join(app.config['BASEDIR'], 'app/plugins/')
    dirs = os.listdir(plugins_directory)
    plugins = []

    for directory in dirs:
        if os.path.isdir(os.path.join(plugins_directory,directory)):
            plugins.append(directory)

    return plugins

