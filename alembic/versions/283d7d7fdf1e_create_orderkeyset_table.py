"""create OrderKeySet table

Revision ID: 283d7d7fdf1e
Revises: 
Create Date: 2020-09-07 18:22:57.909503

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '283d7d7fdf1e'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'orderkeyset',
        sa.Column('order_id', sa.Integer, primary_key=True),
        sa.Column('dispatcher_key', sa.String(20), nullable=False),
        sa.Column('driver_key', sa.String(20), nullable=False),
        sa.Column('customer_key', sa.String(20), nullable=False),
    )


def downgrade():
    op.drop_table('orderkeyset')
