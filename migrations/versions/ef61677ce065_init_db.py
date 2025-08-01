"""Init DB

Revision ID: ef61677ce065
Revises: 
Create Date: 2025-08-01 18:54:01.685886

"""
from typing import Sequence, Union

import geoalchemy2
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'ef61677ce065'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('activity',
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('lft', sa.Integer(), nullable=False),
    sa.Column('rgt', sa.Integer(), nullable=False),
    sa.Column('parent_id', sa.UUID(), nullable=True),
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
    sa.ForeignKeyConstraint(['parent_id'], ['activity.id'], ondelete='SET NULL'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_activity_lft'), 'activity', ['lft'], unique=False)
    op.create_index(op.f('ix_activity_rgt'), 'activity', ['rgt'], unique=False)
    op.create_table('building',
    sa.Column('adress', sa.String(), nullable=False),
    sa.Column('cords', geoalchemy2.types.Geometry(geometry_type='POINT', dimension=2, spatial_index=False, from_text='ST_GeomFromEWKT', name='geometry', nullable=False), nullable=False),
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('organization',
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('activity_id', sa.UUID(), nullable=False),
    sa.Column('building_id', sa.UUID(), nullable=False),
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
    sa.ForeignKeyConstraint(['activity_id'], ['activity.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['building_id'], ['building.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('organization')
    op.drop_table('building')
    op.drop_index(op.f('ix_activity_rgt'), table_name='activity')
    op.drop_index(op.f('ix_activity_lft'), table_name='activity')
    op.drop_table('activity')
    # ### end Alembic commands ###
