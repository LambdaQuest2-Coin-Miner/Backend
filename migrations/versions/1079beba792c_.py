"""empty message

Revision ID: 1079beba792c
Revises: 
Create Date: 2020-02-27 08:25:05.500865

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1079beba792c'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('rooms',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(), nullable=True),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('coordinates', sa.String(), nullable=True),
    sa.Column('exits', sa.String(), nullable=True),
    sa.Column('cooldown', sa.Numeric(), nullable=True),
    sa.Column('errors', sa.String(), nullable=True),
    sa.Column('messages', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('players',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('encumbrance', sa.Integer(), nullable=True),
    sa.Column('strength', sa.Integer(), nullable=True),
    sa.Column('speed', sa.Integer(), nullable=True),
    sa.Column('gold', sa.Integer(), nullable=True),
    sa.Column('bodywear', sa.String(), nullable=True),
    sa.Column('footwear', sa.String(), nullable=True),
    sa.Column('inventory', sa.String(), nullable=True),
    sa.Column('status', sa.String(), nullable=True),
    sa.Column('current_room_id', sa.Integer(), nullable=True),
    sa.Column('last_room_visited_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['current_room_id'], ['rooms.id'], ),
    sa.ForeignKeyConstraint(['last_room_visited_id'], ['rooms.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('players')
    op.drop_table('rooms')
    # ### end Alembic commands ###
