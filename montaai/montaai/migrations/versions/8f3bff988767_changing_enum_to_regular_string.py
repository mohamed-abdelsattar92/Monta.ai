"""Changing enum to regular string

Revision ID: 8f3bff988767
Revises: 3de123b2b1a8
Create Date: 2024-05-14 22:04:48.472956

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '8f3bff988767'
down_revision = '3de123b2b1a8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('message', schema=None) as batch_op:
        batch_op.alter_column('role',
               existing_type=postgresql.ENUM('USER', name='messagerole'),
               type_=sa.String(length=80),
               existing_nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('message', schema=None) as batch_op:
        batch_op.alter_column('role',
               existing_type=sa.String(length=80),
               type_=postgresql.ENUM('USER', name='messagerole'),
               existing_nullable=False)

    # ### end Alembic commands ###