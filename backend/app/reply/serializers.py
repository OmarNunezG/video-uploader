from django.contrib.auth import get_user_model
from rest_framework import serializers
from core import models


class ReplySerializer(serializers.ModelSerializer):
    """Serializer for the Reply model."""

    class Meta:
        model = models.CommentReply
        fields = (
            "id",
            "text",
            "comment",
            "likes",
            "created_by",
        )

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        created_by = get_user_model().objects.get(
            id=representation["created_by"]
        )
        representation["created_by"] = created_by.username
        return representation
