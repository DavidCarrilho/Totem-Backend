"""Created location column on Store and removed enabled

Revision ID: 72fe99a6bf4d
Revises: 
Create Date: 2025-05-05 23:07:16.800353

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '72fe99a6bf4d'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('stores', sa.Column('location', sa.String(), nullable=True, server_default=''))
    op.drop_column('stores', 'enabled')  # <-- assumindo que você queria remover 'enabled'

def downgrade() -> None:
    """Downgrade schema."""
    op.add_column('stores', sa.Column('enabled', sa.Boolean(), nullable=True))
    op.drop_column('stores', 'location')

