"""Added skill, job and relationship models

Revision ID: e4f9c6206df2
Revises: bf30be0299bd
Create Date: 2025-05-07 22:23:38.535486

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e4f9c6206df2'
down_revision = 'bf30be0299bd'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('job',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=128), nullable=True),
    sa.Column('company', sa.String(length=128), nullable=True),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('location', sa.String(length=128), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('job', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_job_title'), ['title'], unique=False)

    op.create_table('skill_category',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('skill_category', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_skill_category_name'), ['name'], unique=True)

    op.create_table('skill',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.Column('description', sa.String(length=256), nullable=True),
    sa.Column('category_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['category_id'], ['skill_category.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('skill', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_skill_name'), ['name'], unique=True)

    op.create_table('job_skills',
    sa.Column('job_id', sa.Integer(), nullable=True),
    sa.Column('skill_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['job_id'], ['job.id'], ),
    sa.ForeignKeyConstraint(['skill_id'], ['skill.id'], )
    )
    op.create_table('user_skills',
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('skill_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['skill_id'], ['skill.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], )
    )
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('first_name', sa.String(length=64), nullable=True))
        batch_op.add_column(sa.Column('last_name', sa.String(length=64), nullable=True))
        batch_op.add_column(sa.Column('created_at', sa.DateTime(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_column('created_at')
        batch_op.drop_column('last_name')
        batch_op.drop_column('first_name')

    op.drop_table('user_skills')
    op.drop_table('job_skills')
    with op.batch_alter_table('skill', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_skill_name'))

    op.drop_table('skill')
    with op.batch_alter_table('skill_category', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_skill_category_name'))

    op.drop_table('skill_category')
    with op.batch_alter_table('job', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_job_title'))

    op.drop_table('job')
    # ### end Alembic commands ###
