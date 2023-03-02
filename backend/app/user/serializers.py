from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.serializers import (
    TokenObtainPairSerializer,
    TokenRefreshSerializer,
)
from core import models


class PairTokenSerializer(TokenObtainPairSerializer):
    """Pair token serializer"""

    def to_representation(self, instance):
        """Custom representation of the token"""

        data = super().to_representation(instance)
        representation = {
            "attributes": {
                "access": data["access"],
                "refresh": data["refresh"],
            },
        }
        return representation


class RefreshTokenSerializer(TokenRefreshSerializer):
    """Refresh token serializer"""

    def to_representation(self, instance):
        """Custom representation of the token"""

        data = super().to_representation(instance)
        representation = {
            "attributes": {
                "access": data["access"],
            },
        }
        return representation


class UserSerializer(serializers.ModelSerializer):
    """User serializer"""

    date_joined = serializers.SerializerMethodField()

    class Meta:
        model = get_user_model()
        fields = (
            "id",
            "first_name",
            "middle_name",
            "last_name",
            "email",
            "username",
            "password",
            "date_joined",
        )
        extra_kwargs = {
            "id": {
                "read_only": True,
            },
            "password": {
                "write_only": True,
                "min_length": 8,
            },
        }

    def get_date_joined(self, obj):
        """Get the date when the user joined"""

        return obj.date_joined.strftime("%m-%d-%Y %H:%M:%S")

    def to_representation(self, instance):
        """Custom representation of the user"""

        data = super().to_representation(instance)
        representation = {
            "id": data["id"],
            "attributes": {k: v for k, v in data.items() if k != "id"},
        }
        return representation


class UserVideoSerializer(serializers.ModelSerializer):
    """User video serializer"""

    created_by = serializers.SerializerMethodField()

    class Meta:
        model = models.Video
        fields = "__all__"
        read_only_fields = ("id",)

    def to_representation(self, instance):
        """Custom representation of the user"""

        data = super().to_representation(instance)
        representation = {
            "id": data["id"],
            "attributes": {
                k: v
                for k, v in data.items()
                if k != "id" and k != "created_by"
            },
            "created_by": data["created_by"],
        }

        return representation

    def get_created_by(self, obj):
        """Get the user who created the video"""

        return obj.created_by.username
