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
import json

class Plugins():
        def __init__(self, app):
            self.plugins_directory = os.path.join(app.config['BASEDIR'], 'app/plugins/')
            self.plugins = []

	def init_plugins(self):
	    dirs = os.listdir(self.plugins_directory)

	    for directory in dirs:
		if os.path.isdir(os.path.join(self.plugins_directory,directory)):
                    plugins_information = os.path.join(self.plugins_directory,directory + '/plugin.json')
		    if os.path.isfile(plugins_information):
			json_data = open(plugins_information)
			data = json.load(json_data)
			self.plugins.append((directory, data))


	def register_plugins(self, app):
            plugins_list = []
	    try:
		for plugin, data in self.plugins:
		    exec("from app.plugins.%s.views import %s" %(plugin, plugin))
		    exec("app.register_blueprint(%s)" % plugin)
		    plugins_list.append(data)
	    except ImportError, e:
		print "Can't register plugin : %s" % e

            return plugins_list
