from rest_framework import serializers
from core import models


class CommentSerializer(serializers.ModelSerializer):
    created_at = serializers.SerializerMethodField()
    created_by = serializers.SerializerMethodField()

    class Meta:
        model = models.Comment
        fields = "__all__"
        read_only_fields = ("id", "created_at", "created_by", "likes")

    def get_created_at(self, obj):
        return obj.created_at.strftime("%Y-%m-%d %H:%M:%S")

    def get_created_by(self, obj):
        return obj.created_by.username


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CommentLike
        fields = "__all__"
        read_only_fields = ("id",)

    def create(self, validated_data):
        comment = validated_data["comment"]
        comment.likes += 1
        comment.save()

        return super().create(validated_data)

    def delete(self, instance):
        comment = instance.comment
        comment.likes -= 1
        comment.save()

        instance.delete()
