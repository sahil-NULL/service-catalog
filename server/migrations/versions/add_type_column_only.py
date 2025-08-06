"""Add type column to system_components only

Revision ID: add_type_column_only
Revises: e4344023243d
Create Date: 2025-08-06 17:35:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'add_type_column_only'
down_revision: Union[str, Sequence[str], None] = 'e4344023243d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Add type column to system_components table."""
    # Add the type column to system_components table
    op.add_column('system_components', sa.Column('type', sa.String(), nullable=False, server_default='direct'))


def downgrade() -> None:
    """Remove type column from system_components table."""
    # Remove the type column from system_components table
    op.drop_column('system_components', 'type') 