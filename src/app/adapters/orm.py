import logging

import sqlalchemy as sa
from sqlalchemy import orm
from sqlalchemy.orm import registry

from src.app.domain import model

logger = logging.getLogger(__name__)


mapper_registry = registry()
metadata = mapper_registry.metadata

comments = sa.Table(
    "comments",
    metadata,
    sa.Column("id", sa.String, primary_key=True),
    sa.Column("source_id", sa.String),
    sa.Column("source_type", sa.String),
    # """
    # sa.Column("post_id", sa.String),
    # sa.Column("comment_id", sa.String, nullable=True),
    # """,
    sa.Column("content", sa.String),
    sa.Column("created_time", sa.TIMESTAMP),
    sa.Column("updated_time", sa.TIMESTAMP),
    sa.Column("version", sa.Integer),
    sa.Column("author_id", sa.String),
)


posts = sa.Table(
    "posts",
    metadata,
    sa.Column("id", sa.String, primary_key=True),
    sa.Column("title", sa.String),
    sa.Column("content", sa.String),
    sa.Column("created_time", sa.TIMESTAMP),
    sa.Column("updated_time", sa.TIMESTAMP),
    sa.Column("version", sa.Integer),
    sa.Column("author_id", sa.String),
)

likes = sa.Table(
    "likes",
    metadata,
    sa.Column("id", sa.String, primary_key=True),
    sa.Column("source_id", sa.String),
    sa.Column("source_type", sa.String),
    sa.Column("user_id", sa.String),
)


def start_mappers() -> None:
    """
    This method starts the mappers.
    """
    # logger.info("Starting mappers")
    like_mapper = mapper_registry.map_imperatively(
        class_=model.Like,
        local_table=likes,
    )

    comment_mapper = mapper_registry.map_imperatively(
        class_=model.Comment,
        local_table=comments,
    )

    post_mapper = mapper_registry.map_imperatively(
        class_=model.Post,
        local_table=posts,
    )

    comment_mapper.add_properties(
        {
            "replies": orm.relationship(
                argument=comment_mapper,
                primaryjoin=(
                    sa.and_(
                        comments.c.id == comments.c.source_id, comments.c.source_type == "comment"
                    )
                ),
                backref="comment",
                collection_class=list,
                lazy="select",
            ),
            "likes": orm.relationship(
                argument=like_mapper,
                primaryjoin=(
                    sa.and_(comments.c.id == likes.c.source_id, likes.c.source_type == "comment")
                ),
                backref="comment",
                collection_class=list,
                lazy="select",
            ),
            "like_count": orm.column_property(sa.func.count("likes").label("like_count")),
        }
    )

    post_mapper.add_properties(
        {
            "comments": orm.relationship(
                argument=comment_mapper,
                primaryjoin=(
                    sa.and_(posts.c.id == comments.c.source_id, comments.c.source_type == "post")
                ),
                backref="post",
                collection_class=list,
                lazy="select",
            ),
            "likes": orm.relationship(
                argument=like_mapper,
                primaryjoin=(
                    sa.and_(posts.c.id == likes.c.source_id, likes.c.source_type == "post")
                ),
                backref="post",
                collection_class=list,
                lazy="select",
            ),
            "like_count": orm.column_property(sa.func.count("likes").label("like_count")),
        }
    )

    metadata.create_all(bind=sa.create_engine("postgresql://postgres:postgres@localhost:5432/db"))
