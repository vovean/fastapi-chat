"""tabe for last read message for every chat

Revision ID: b95f5892acec
Revises: 63d833b96a44
Create Date: 2020-09-15 23:08:02.036201

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
from sqlalchemy import ForeignKey
from sqlalchemy.sql import expression

revision = 'b95f5892acec'
down_revision = '63d833b96a44'
branch_labels = None
depends_on = None


def upgrade():
    op.drop_column("messages", "watched")
    op.create_table(
        'read_messages',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('order_id', sa.Integer, ForeignKey('orderkeyset.order_id')),
        sa.Column('chat_type', sa.String(20)),
        sa.Column('role', sa.String(20)),
        sa.Column('last_read_message_id', sa.Integer, ForeignKey('messages.id')),
    )
    op.create_unique_constraint('uq_order_chat_role', 'read_messages', ['order_id', 'chat_type', 'role'])


def downgrade():
    op.add_column(
        "messages",
        sa.Column('watched', sa.Boolean, server_default=expression.false(), nullable=False)
    )
    op.drop_unique_constraint('uq_order_chat_role')
    op.drop_table('read_messages')
