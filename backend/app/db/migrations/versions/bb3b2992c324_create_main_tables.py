"""create_main_tables
Revision ID: bb3b2992c324
Revises: 
Create Date: 2021-07-14 17:47:08.487373
"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic
revision = 'bb3b2992c324'
down_revision = None
branch_labels = None
depends_on = None


def create_posts_table() -> None:
    op.create_table(
        "posts",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("extracted_at", sa.DateTime, nullable=False, index=True),
        sa.Column('name', sa.Text, index=True),
        sa.Column("post_id", sa.Text, nullable=False, unique=True, index=True),
        sa.Column("title", sa.Text, nullable=False),
        sa.Column("score", sa.Integer, nullable=False),
        sa.Column("url", sa.Text, nullable=False),
        sa.Column("author", sa.Text, nullable=False),
        sa.Column("subreddit", sa.Text, nullable=False),
        sa.Column("description", sa.Text, nullable=False),
        sa.Column("created_at", sa.DateTime, nullable=False),
        sa.Column("isscore", sa.Boolean, nullable=False, server_default="False")
    )


def create_seriousness_table() -> None:
    op.create_table(
        "seriousness",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("model_score", sa.Float, nullable=False),
        sa.Column("post_no", sa.Integer, sa.ForeignKey("posts.id", ondelete="CASCADE"))
    )

def upgrade() -> None:
    create_posts_table()
    create_seriousness_table()

def downgrade() -> None:
    op.drop_table("seriousness")
    op.drop_table("posts")
