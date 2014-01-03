"""added user_id column for plugins

Revision ID: 1310f064f386
Revises: None
Create Date: 2014-01-03 09:38:03.663703

"""

# revision identifiers, used by Alembic.
revision = '1310f064f386'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('plugins', sa.Column('user_id', sa.Integer))

def downgrade():
    op.drop_column('plugins', 'user_id')
