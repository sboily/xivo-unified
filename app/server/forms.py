from flask.ext.wtf import Form, TextField, BooleanField, PasswordField, ValidationError
from flask.ext.wtf import Required
from models import Servers

class ServersForm(Form):
    name = TextField('name', validators=[Required()])
    address = TextField('address', validators=[Required()])
    login = TextField('login', validators=[Required()])
    password = PasswordField('password', validators=[Required()])

#    def validate_login(self, field):
#        user = self.get_user()
#
#        if user is None:
#            raise ValidationError('Invalid user')
#
#        if user.password != self.password.data:
#            raise ValidationError('Invalid password')
#
#    def get_user(self):
#        return User(self.login.data, self.password.data)
