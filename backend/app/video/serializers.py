from django.contrib.auth import get_user_model
from rest_framework import serializers
from core import models


class VideoSerializer(serializers.ModelSerializer):
    thumbnail = serializers.SerializerMethodField()
    file = serializers.SerializerMethodField()
    created_at = serializers.SerializerMethodField()
    created_by = serializers.SerializerMethodField()

    class Meta:
        model = models.Video
        fields = "__all__"
        read_only_fields = ("id", "likes", "created_at")

    def update(self, instance, validated_data):
        validated_data.pop("file", None)
        validated_data.pop("likes", None)
        validated_data.pop("created_by", None)
        validated_data.pop("created_at", None)

        return super().update(instance, validated_data)

    def get_thumbnail(self, obj):
        thumbnail = obj.thumbnail
        created_by = obj.created_by.id

        url = f"/media/{created_by}/thumbnails/{thumbnail}"
        return url

    def get_file(self, obj):
        file = obj.file
        created_by = obj.created_by.id

        url = f"/media/{created_by}/videos/{file}"
        return url

    def get_created_at(self, obj):
        return obj.created_at.strftime("%Y-%m-%d %H:%M:%S")

    def get_created_by(self, obj):
        user = obj.created_by
        return user.username


class CommentSerializer(serializers.ModelSerializer):
    """Serializer for video comments"""

    created_at = serializers.SerializerMethodField()
    created_by = serializers.SerializerMethodField()

    class Meta:
        model = models.Comment
        fields = "__all__"
        read_only_fields = ("id", "created_at", "created_by", "likes")

    def get_created_at(self, obj):
        return obj.created_at.strftime("%Y-%m-%d %H:%M:%S")

    def get_created_by(self, obj):
        user = obj.created_by
        return user.username


class LikeSerializer(serializers.ModelSerializer):
    """Serializer for video likes"""

    class Meta:
        model = models.VideoLike
        fields = "__all__"
        read_only_fields = ("id",)

    def create(self, validated_data):
        """Creates a new like and updates the video likes count"""
        video_id = validated_data["video"]
        video = models.Video.objects.get(id=video_id)
        video.likes += 1
        video.save()

        user_id = validated_data["liked_by"]
        user = get_user_model().objects.get(id=user_id)

        validated_data["video"] = video
        validated_data["liked_by"] = user

        return super().create(validated_data)

    def delete(self, instance):
        """Deletes a like and updates the video likes count"""
        video = instance.video
        video.likes -= 1
        video.save()

        instance.delete()
