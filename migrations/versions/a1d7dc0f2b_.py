"""empty message

Revision ID: a1d7dc0f2b
Revises: None
Create Date: 2015-08-29 17:10:02.458791

"""

# revision identifiers, used by Alembic.
revision = 'a1d7dc0f2b'
down_revision = None

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('moves',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('type', sa.String(), nullable=True),
    sa.Column('category', sa.String(), nullable=True),
    sa.Column('power', sa.Integer(), nullable=True),
    sa.Column('pp', sa.Integer(), nullable=True),
    sa.Column('accuracy', sa.Integer(), nullable=True),
    sa.Column('effect', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('natures',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('bonus', sa.String(), nullable=True),
    sa.Column('penalty', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('pokemon',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('stats', postgresql.JSON(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('pokemon_moves',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('pokemon_id', sa.Integer(), nullable=True),
    sa.Column('move_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['move_id'], ['moves.id'], ),
    sa.ForeignKeyConstraint(['pokemon_id'], ['pokemon.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('pokemon_moves')
    op.drop_table('pokemon')
    op.drop_table('natures')
    op.drop_table('moves')
    ### end Alembic commands ###
