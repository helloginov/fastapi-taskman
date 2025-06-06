"""complexity

Revision ID: d259f09f4c90
Revises: db9eb9ef81d8
Create Date: 2025-05-06 14:37:51.465895

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = 'd259f09f4c90'
down_revision: Union[str, None] = 'db9eb9ef81d8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('productivitylog', sa.Column('tasks_completed_month', sa.Integer(), nullable=False, server_default=sa.text('0')))
    op.add_column('productivitylog', sa.Column('mean_complexity_month', sa.Float(), nullable=False, server_default=sa.text('0.0')))
    op.add_column('task', sa.Column('complexity', sa.Integer(), nullable=False, server_default=sa.text('1')))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('task', 'complexity')
    op.drop_column('productivitylog', 'mean_complexity_month')
    op.drop_column('productivitylog', 'tasks_completed_month')
    # ### end Alembic commands ###
