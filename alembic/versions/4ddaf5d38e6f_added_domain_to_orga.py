"""Added domain to organisations

Revision ID: 4ddaf5d38e6f
Revises: 1310f064f386
Create Date: 2014-01-05 14:15:01.000253

"""

# revision identifiers, used by Alembic.
revision = '4ddaf5d38e6f'
down_revision = '1310f064f386'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('organisations', sa.Column('domain', sa.String(300)))

def downgrade():
    op.drop_column('organisations', 'domain')
