from flask.ext.login import current_user
from flask import current_app
from functools import wraps

def required_role(role):
    """ Gatekeeper for views

This decorator checks that a user is authenticated
and that they have the required role to access a
view. If either check fails, they are sent
to the current app's login_managers unauthorized
route.

"""

    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if current_user.is_authenticated():
                if role in [x.name for x in current_user.roles]:
                    return f(*args, **kwargs)
            return current_app.login_manager.unauthorized()
        return decorated_function
    return decorator
