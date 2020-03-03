"""nullable text

Revision ID: 79a1885b0902
Revises: 05c5b8da6871
Create Date: 2020-02-01 21:42:19.798711

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '79a1885b0902'
down_revision = '05c5b8da6871'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('new', 'text',
               existing_type=sa.TEXT(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('new', 'text',
               existing_type=sa.TEXT(),
               nullable=False)
    # ### end Alembic commands ###