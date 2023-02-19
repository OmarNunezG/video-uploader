from __future__ import annotations
from django.conf import settings
from django.contrib.auth.models import (
    BaseUserManager,
    AbstractUser,
    PermissionsMixin,
)
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.validators import (
    FileExtensionValidator,
    RegexValidator,
    MinValueValidator,
)
from django.db import models
from django.utils.translation import gettext_lazy as _
import os
from uuid import uuid4
from core.validators import MaxSizeValidator

allowed_thumbnail_extensions = ("jpg", "jpeg", "png")
allowed_video_extensions = ("mp4",)


def generate_filename(instance, filename):
    """Generate a random filename with the same extension as the original."""
    ext = filename.split(".")[-1]
    type = "thumbails"
    for allowed_ext in allowed_video_extensions:
        if ext == allowed_ext:
            type = "videos"
            break

    filename = f"{uuid4()}.{ext}"
    return os.path.join(f"{instance.created_by.id}", type, filename)


class UserManager(BaseUserManager):
    """Custom user manager."""

    def create(
        self,
        first_name: str,
        last_name: str,
        username: str,
        email: str,
        password: str,
        middle_name: str = None,
    ) -> User:
        """Create a new user with the given details."""

        user = self.model(
            first_name=first_name,
            middle_name=middle_name,
            last_name=last_name,
            username=username,
            email=email,
            password=password,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(
        self,
        first_name: str,
        last_name: str,
        username: str,
        email: str,
        password: str,
        middle_name: str = None,
    ) -> User:
        """Create a new superuser with the given details."""

        user = self.create(
            first_name, last_name, username, email, password, middle_name
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

    def normalize_email(self, email: str) -> str:
        """Normalize the email address by lowercasing the given address."""

        return email.lower()


class User(AbstractUser, PermissionsMixin):
    """Custom user model."""

    id = models.BigAutoField(
        verbose_name=_("id"), primary_key=True, unique=True, editable=False
    )
    first_name = models.CharField(verbose_name=_("first name"), max_length=50)
    middle_name = models.CharField(
        verbose_name=_("middle name"), max_length=50, null=True, blank=True
    )
    last_name = models.CharField(verbose_name=_("last name"), max_length=50)
    username = models.CharField(
        verbose_name=_("username"),
        max_length=20,
        unique=True,
        validators=[UnicodeUsernameValidator],
    )
    email = models.EmailField(
        verbose_name=_("email"), max_length=255, unique=True
    )
    date_joined = models.DateTimeField(
        _("date joined"), auto_now_add=True, editable=False
    )

    objects = UserManager()

    REQUIRED_FIELDS = ["first_name", "last_name", "email"]

    def __str__(self) -> str:
        return self.username


class Video(models.Model):
    """Model for videos."""

    id = models.BigAutoField(
        verbose_name=_("id"), primary_key=True, unique=True, editable=False
    )
    title = models.CharField(verbose_name=_("title"), max_length=100)
    description = models.TextField(
        verbose_name=_("description"), max_length=5000, null=True, blank=True
    )
    thumbnail = models.ImageField(
        verbose_name=_("thumbnail"),
        upload_to=generate_filename,
        validators=[
            FileExtensionValidator(
                allowed_extensions=["jpg", "jpeg", "png"],
                message="File must be jpg, jpeg or png.",
            ),
            MaxSizeValidator(
                1 * 1024 * 1024, message="File size cannot exceed 1 MB."
            ),
        ],
    )
    file = models.FileField(
        verbose_name=_("file"),
        upload_to=generate_filename,
        validators=[
            FileExtensionValidator(
                allowed_extensions=["mp4"], message="File must be mp4."
            ),
            MaxSizeValidator(
                10 * 1024 * 1024, message="File size cannot exceed 10 MB."
            ),
        ],
    )
    likes = models.IntegerField(verbose_name=_("likes"), default=0)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_("Uploaded by"),
        on_delete=models.CASCADE,
    )
    created_at = models.DateTimeField(
        verbose_name=_("Uploaded at"), auto_now_add=True, editable=False
    )

    class Meta:
        verbose_name = _("video")
        verbose_name_plural = _("videos")
        db_table = "video"

    def __str__(self) -> str:
        return self.title


class Comment(models.Model):
    """Model for comment.s"""

    id = models.BigAutoField(
        verbose_name=_("id"), primary_key=True, unique=True, editable=False
    )
    text = models.TextField(verbose_name=_("Comment"), max_length=255)
    video = models.ForeignKey(
        Video,
        verbose_name=_("video"),
        on_delete=models.CASCADE,
        related_query_name="comment",
    )
    likes = models.IntegerField(
        verbose_name=_("likes"), default=0, validators=[MinValueValidator(0)]
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_("Commented by"),
        on_delete=models.CASCADE,
        related_query_name="comment",
    )
    created_at = models.DateTimeField(
        verbose_name=_("created at"), auto_now_add=True, editable=False
    )

    class Meta:
        verbose_name = _("comment")
        verbose_name_plural = _("comments")
        db_table = "comment"

    def __str__(self) -> str:
        return self.text[:20]


class VideoLike(models.Model):
    """Model for likes attached to videos."""

    id = models.BigAutoField(
        verbose_name=_("id"), primary_key=True, unique=True, editable=False
    )
    video = models.ForeignKey(
        Video,
        verbose_name=_("video"),
        on_delete=models.CASCADE,
        related_query_name="video_like",
    )
    liked_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_("liked by"),
        on_delete=models.CASCADE,
        related_query_name="video_like",
    )

    class Meta:
        verbose_name = _("video like")
        verbose_name_plural = _("video likes")
        db_table = "video_like"
        unique_together = ("video", "liked_by")

    def __str__(self) -> str:
        return self.video.title


class VideoTag(models.Model):
    """Model for tags attached to videos."""

    id = models.BigAutoField(
        verbose_name=_("id"), primary_key=True, unique=True, editable=False
    )
    video = models.ForeignKey(
        Video,
        verbose_name=_("video"),
        on_delete=models.CASCADE,
        related_query_name="video_tag",
    )
    tag = models.CharField(
        verbose_name=_("tag"),
        max_length=50,
        validators=[RegexValidator(r"^[a-zA-Z0-9_]+$")],
    )

    class Meta:
        verbose_name = _("video tag")
        verbose_name_plural = _("video tags")
        db_table = "video_tag"
        unique_together = ("video", "tag")

    def __str__(self) -> str:
        return self.video.title


class CommentLike(models.Model):
    """Model for likes attached to comments."""

    id = models.BigAutoField(
        verbose_name=_("id"), primary_key=True, unique=True, editable=False
    )
    comment = models.ForeignKey(
        Comment,
        verbose_name=_("comment"),
        on_delete=models.CASCADE,
        related_query_name="comment_like",
    )
    liked_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_("liked by"),
        on_delete=models.CASCADE,
        related_query_name="comment_like",
    )

    class Meta:
        verbose_name = _("comment like")
        verbose_name_plural = _("comment likes")
        db_table = "comment_like"
        unique_together = ("comment", "liked_by")

    def __str__(self) -> str:
        return self.comment.created_by.username


class CommentReply(models.Model):
    id = models.BigAutoField(primary_key=True, unique=True, editable=False)
    text = models.TextField(verbose_name=_("text"), max_length=1000)
    comment = models.ForeignKey(
        Comment,
        related_query_name="comment_reply",
        on_delete=models.CASCADE,
    )
    likes = models.IntegerField(verbose_name=_("likes"), default=0)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_("Replied by"),
        on_delete=models.CASCADE,
        related_query_name="comment_reply",
    )
    created_at = models.DateTimeField(
        verbose_name=_("Replied at"), auto_now_add=True, editable=False
    )


class ReplyLike(models.Model):
    id = models.BigAutoField(primary_key=True, unique=True, editable=False)
    reply = models.ForeignKey(
        CommentReply,
        related_query_name="reply_like",
        on_delete=models.CASCADE,
    )
    liked_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_("liked by"),
        on_delete=models.CASCADE,
        related_query_name="reply_like",
    )

    class Meta:
        verbose_name = _("reply like")
        verbose_name_plural = _("reply likes")
        db_table = "reply_like"
        unique_together = ("reply", "liked_by")

    def __str__(self) -> str:
        return self.reply.created_by.username
