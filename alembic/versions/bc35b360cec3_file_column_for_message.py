"""file column for message

Revision ID: bc35b360cec3
Revises: b95f5892acec
Create Date: 2020-09-16 13:59:51.805141

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'bc35b360cec3'
down_revision = 'b95f5892acec'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        'messages',
        sa.Column("file_path", sa.String(70), nullable=True)
    )


def downgrade():
    op.drop_column('messages', 'file_path')
