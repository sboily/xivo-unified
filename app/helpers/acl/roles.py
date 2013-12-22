
from flask.ext.principal import Permission, RoleNeed

# Configure roles
root_role = Permission(RoleNeed('root'))
manager_role = Permission(RoleNeed('manager')).union(root_role)
admin_role = Permission(RoleNeed('admin')).union(manager_role)
