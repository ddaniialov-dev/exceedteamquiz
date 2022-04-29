"""ordering fix

Revision ID: 3453bb53fafe
Revises: 6cf3fa8b3f96
Create Date: 2022-04-28 14:57:53.220676

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "3453bb53fafe"
down_revision = "6cf3fa8b3f96"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("questions", sa.Column("ordering", sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("questions", "ordering")
    # ### end Alembic commands ###
