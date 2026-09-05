"""empty message

Revision ID: 26b962af7447
Revises: 66c314fac6db
Create Date: 2026-09-04 11:48:44.912480

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "26b962af7447"
down_revision: Union[str, Sequence[str], None] = "66c314fac6db"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.alter_column("brands", "origen", new_column_name="origin")


def downgrade() -> None:
    """Downgrade schema."""
    op.alter_column("brands", "origin", new_column_name="origen")
