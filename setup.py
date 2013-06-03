#!/usr/bin/python

from app import app, db
from app.login.models import User, Role
from app.server.models import Servers

def populate_db():
    db.drop_all()
    db.create_all()
    app.test_request_context().push()

    ua = User('sboily@proformatique.com','Sylvain Boily','superpass')
    sa = Servers('Sylvain Raspberry PI','192.168.1.123','root', 'superpass')

    ra = Role('admin')
    rb = Role('user')
    rc = Role('manager')

    ua.roles = [ra]

    db.session.add_all([ua,sa])
    db.session.commit()

if __name__ == '__main__':
    populate_db()
