"""create Message

Revision ID: 63d833b96a44
Revises: 283d7d7fdf1e
Create Date: 2020-09-10 17:54:54.893695

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
from sqlalchemy import ForeignKey

revision = '63d833b96a44'
down_revision = '283d7d7fdf1e'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'messages',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('order_id', sa.Integer, ForeignKey('orderkeyset.order_id')),
        sa.Column('sender_token', sa.String(20)),
        sa.Column('sent_at', sa.DateTime, server_default=sa.func.current_timestamp()),
        sa.Column('text', sa.String(300)),
    )


def downgrade():
    op.drop_table('messages')
