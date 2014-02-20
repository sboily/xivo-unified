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
WTF_CSRF_ENABLED = True
SECRET_KEY = "XiVO_YEAH_GPLv3"
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASEDIR, 'db/xivo.db')
SQLALCHEMY_ECHO = False
SQLALCHEMY_BINDS = {}
DATABASE_CONNECT_OPTIONS = {}
BABEL_DEFAULT_LOCALE = 'en'
BROKER_URL = 'amqp://guest@localhost:5672//'
CELERY_RESULT_BACKEND = 'amqp'
CELERY_SEND_TASK_SENT_EVENT = True
CELERY_TRACK_STARTED = True
COUCHDB_SERVER = 'http://localhost:5984/'
COUCHDB_DATABASE = 'xivo-unified'
AYAH_PUBLISHER_KEY = 'e8b4ce4bc37f1b2c3a5aa36fb8010ce287d1ba13'
AYAH_SCORING_KEY = '52487de8cc032a26a17c8ff1fcb9c6fb0adc55e2'
MAIL_DEBUG = False
