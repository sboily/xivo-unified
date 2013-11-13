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

from restclient import GET, POST, PUT, DELETE
import json

class RestClient(object):

    def __init__(self, username, password):
        self.httplib_params = {'timeout': 10, 'disable_ssl_certificate_validation' : True}
        self.headers = {'Content-Type': 'application/json'}
        self.username = username
        self.password = password

    def _check_response(self, data):
        http_code = int(data[0]['status'])

        if (http_code >= 300):
            return False

        try:
            return json.loads(data[1])
        except:
            print "No json information"
        

    def actions(self, url, method, data=None):
        if (method == 'GET'):
            data = GET(url, credentials=(self.username, self.password),
                                headers=self.headers,
                                httplib_params=self.httplib_params,
                                resp=True)
        elif (method == 'DELETE'):
            data = DELETE(url, credentials=(self.username, self.password),
                                   headers=self.headers,
                                   httplib_params=self.httplib_params,
                                   async=False,
                                   resp=True)
        elif (method == 'POST'):
            data = POST(url, credentials=(self.username, self.password),
                                 headers=self.headers,
                                 httplib_params=self.httplib_params,
                                 params=data,
                                 async=False,
                                 resp=True)
        elif (method == 'PUT'):
            data = PUT(url, credentials=(self.username, self.password),
                                 headers=self.headers,
                                 httplib_params=self.httplib_params,
                                 params=data,
                                 async=False,
                                 resp=True)
        else:
            print "Error this method is not supported"
            return False

        return self._check_response(data)
