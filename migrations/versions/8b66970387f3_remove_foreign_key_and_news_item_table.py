"""Remove foreign key and news_item table

Revision ID: 8b66970387f3
Revises: 6e06d19f827d
Create Date: 2025-04-24 13:41:44.210575

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8b66970387f3'
down_revision = '6e06d19f827d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('news_item')
    with op.batch_alter_table('slider_item', schema=None) as batch_op:
        batch_op.drop_column('news_id')
        batch_op.drop_column('link')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('slider_item', schema=None) as batch_op:
        batch_op.add_column(sa.Column('link', sa.VARCHAR(length=200), nullable=True))
        batch_op.add_column(sa.Column('news_id', sa.INTEGER(), nullable=True))

    op.create_table('news_item',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('title', sa.VARCHAR(length=200), nullable=False),
    sa.Column('slug', sa.VARCHAR(length=200), nullable=False),
    sa.Column('content', sa.TEXT(), nullable=True),
    sa.Column('image', sa.VARCHAR(length=200), nullable=True),
    sa.Column('created_at', sa.DATETIME(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('slug')
    )
    # ### end Alembic commands ###
