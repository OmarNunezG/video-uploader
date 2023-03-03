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
