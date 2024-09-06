"""renaming some columns in User model

Revision ID: 13f9d04bf182
Revises: f0622e10d2d9
Create Date: 2024-08-09 22:25:45.501109

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '13f9d04bf182'
down_revision = 'f0622e10d2d9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('firstname', sa.String(), nullable=True))
        batch_op.add_column(sa.Column('lastname', sa.String(), nullable=True))
        batch_op.add_column(sa.Column('phonenumber', sa.String(), nullable=True))
        batch_op.drop_column('last_name')
        batch_op.drop_column('first_name')
        batch_op.drop_column('phone_number')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('phone_number', sa.INTEGER(), autoincrement=False, nullable=True))
        batch_op.add_column(sa.Column('first_name', sa.VARCHAR(), autoincrement=False, nullable=True))
        batch_op.add_column(sa.Column('last_name', sa.VARCHAR(), autoincrement=False, nullable=True))
        batch_op.drop_column('phonenumber')
        batch_op.drop_column('lastname')
        batch_op.drop_column('firstname')

    # ### end Alembic commands ###