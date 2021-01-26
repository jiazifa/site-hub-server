"""empty message

Revision ID: 9fa4755ba8b6
Revises: 
Create Date: 2021-01-25 18:25:32.047467

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9fa4755ba8b6'
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
    op.create_table('login_record_model',
    sa.Column('record_id', sa.INTEGER(), nullable=False, comment='用户的登录记录'),
    sa.Column('user_id', sa.INTEGER(), nullable=True),
    sa.Column('op_time', sa.DateTime(), nullable=True),
    sa.Column('op_ip', sa.String(length=20), nullable=True),
    sa.PrimaryKeyConstraint('record_id')
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
    op.create_table('user',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('identifier', sa.String(length=64), nullable=True, comment='用户的唯一标识符'),
    sa.Column('sex', sa.SMALLINT(), nullable=True, comment='0 未设置 1 男性 2 女性'),
    sa.Column('phone', sa.String(length=11), nullable=True, comment='手机号'),
    sa.Column('nickname', sa.String(length=18), nullable=True, comment='用户昵称'),
    sa.Column('email', sa.String(length=64), nullable=True),
    sa.Column('description', sa.String(length=64), nullable=True, comment='个人简介'),
    sa.Column('password', sa.String(length=64), nullable=True),
    sa.Column('token', sa.String(length=64), nullable=True),
    sa.Column('status', sa.SMALLINT(), nullable=True, comment='0 未激活 1 正常 2 异常 3 注销'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
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
    op.drop_table('user')
    op.drop_table('one_word')
    op.drop_table('login_record_model')
    op.drop_table('category')
    # ### end Alembic commands ###