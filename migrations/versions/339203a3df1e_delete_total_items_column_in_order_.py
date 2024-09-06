"""delete total items column in order models

Revision ID: 339203a3df1e
Revises: 13f9d04bf182
Create Date: 2024-08-19 13:38:18.154155

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '339203a3df1e'
down_revision = '13f9d04bf182'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('orders', schema=None) as batch_op:
        batch_op.drop_column('total_items')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('orders', schema=None) as batch_op:
        batch_op.add_column(sa.Column('total_items', sa.INTEGER(), autoincrement=False, nullable=True))

    # ### end Alembic commands ###