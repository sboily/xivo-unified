#!/usr/bin/env python
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


from flask.ext.script import Manager, prompt_bool, Server
from app.extensions import db
from app import create_app

application = create_app()
manager = Manager(application)
manager.add_command("run", Server(host="0.0.0.0", port=5000))

@manager.command
def resetdb():
    """Init/reset database."""

    if not prompt_bool("Are you sure? You will lose all your data!"):
        return

    db.drop_all()
    db.create_all()
    db.session.commit()

if __name__ == "__main__":
    manager.run()
