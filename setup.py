#!/usr/bin/python
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


from app import app, db
from app.login.models import User, Role
from app.server.models import Servers

def populate_db():
    db.drop_all()
    db.create_all()
    app.test_request_context().push()

    ua = User('sboily@proformatique.com','Sylvain Boily','superpass')
    sa = Servers('Sylvain Raspberry PI','192.168.1.123','root','superpass')

    ra = Role('admin')
    rb = Role('user')
    rc = Role('manager')

    ua.roles = [ra]

    db.session.add_all([ua,sa])
    db.session.commit()

if __name__ == '__main__':
    populate_db()
