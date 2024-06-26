import io
import tempfile

import fastapi
import pydantic


class Command(pydantic.BaseModel):
    """
    Base class for all commands.
    """

    model_config = pydantic.ConfigDict(arbitrary_types_allowed=True)


class CreatePostCommand(Command):
    """
    Command for creating a new post.
    """

    title: str
    content: str
    author_id: str


class AttachImageCommand(Command):
    """
    Command for attaching images to a post.
    """

    post_id: str
    user_id: str
    images: list[fastapi.UploadFile] = []


class EditPostCommand(Command):
    """
    Command for editing an existing post.
    """

    user_id: str
    post_id: str
    title: str
    content: str


class LikePostCommand(Command):
    """
    Command for liking a post.
    """

    post_id: str
    user_id: str


class LikeCommentCommand(Command):
    """
    Command for liking a comment.
    """

    comment_id: str
    user_id: str


class CommentPostCommand(Command):
    """
    Command for commenting on a post.
    """

    post_id: str
    user_id: str
    content: str


class ReplyCommentCommand(Command):
    """
    Command for replying to a comment.
    """

    comment_id: str
    user_id: str
    content: str


class DeletePostCommand(Command):
    """
    Command for deleting a post.
    """

    user_id: str
    post_id: str


class DeleteCommentCommand(Command):
    """
    Command for deleting a comment.
    """

    user_id: str
    comment_id: str
