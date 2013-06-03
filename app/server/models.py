from app import db

class Servers(db.Model):
    __tablename__ = 'servers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    address = db.Column(db.String(200))
    login = db.Column(db.String(200))
    password = db.Column(db.String(200))

    def __init__(self, name, address, login, password):
        self.name = name
        self.address = address
        self.login = login
        self.password = password

    def __repr__(self):
        return "<%d : %s (%s)>" % (self.id, self.name, self.address)
