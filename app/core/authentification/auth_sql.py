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

from werkzeug.security import generate_password_hash, check_password_hash
from app.models import User

class UserSql(object):
    def __init__(self, username, passwd):
        self.username = username
        self.passwd = passwd

    def auth(self):
        user = User.query.filter_by(username=self.username).first()
        if user and self.check_passwd(user.password):
            return user

    def check_passwd(self, passwd):
        return check_password_hash(passwd, self.passwd)
