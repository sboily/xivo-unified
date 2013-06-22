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

BASEDIR = os.path.abspath(os.path.dirname(__file__))
DEBUG = True
CSRF_ENABLED = True
SECRET_KEY = "XiVO_YEAH_GPLv3"
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASEDIR, 'db/app.db')
SQLALCHEMY_ECHO = False
SQLALCHEMY_BINDS = {}
DATABASE_CONNECT_OPTIONS = {}
RECAPTCHA_USE_SSL = False
RECAPTCHA_PUBLIC_KEY = '6Lcae-ISAAAAAFXHrh4rgeIus4tjFMumcrbY2xDo'
RECAPTCHA_PRIVATE_KEY = '6Lcae-ISAAAAAK_SSlE-Lrds272ISnizyHJue4M6'
RECAPTCHA_OPTIONS = {'theme': 'white'}
BABEL_DEFAULT_LOCALE = 'en'
