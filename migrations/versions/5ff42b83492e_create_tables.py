"""create_tables

Revision ID: 5ff42b83492e
Revises: 
Create Date: 2021-06-09 18:36:32.516706

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = '5ff42b83492e'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('category',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('name', sa.String(length=128), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('one_word',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('content', sa.TEXT(), nullable=False),
    sa.Column('translate', sa.TEXT(), nullable=True),
    sa.Column('picture', sa.TEXT(), nullable=True),
    sa.Column('create_date', sa.DateTime(), nullable=False),
    sa.Column('author', sa.String(length=64), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('web_site',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('name', sa.String(length=256), nullable=False),
    sa.Column('description', sa.String(length=516), nullable=True),
    sa.Column('url', sa.String(length=516), nullable=False),
    sa.Column('thumb', sa.TEXT(), nullable=True),
    sa.Column('create_date', sa.DateTime(), nullable=False),
    sa.Column('category_id', sa.INTEGER(), nullable=True),
    sa.ForeignKeyConstraint(['category_id'], ['category.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name'),
    sa.UniqueConstraint('url')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('web_site')
    op.drop_table('one_word')
    op.drop_table('category')
    # ### end Alembic commands ###
