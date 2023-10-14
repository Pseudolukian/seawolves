"""sec rev

Revision ID: 73f13fcb149c
Revises: 8fd298dbe3d4
Create Date: 2023-08-29 18:42:12.504805

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '73f13fcb149c'
down_revision: Union[str, None] = '8fd298dbe3d4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
