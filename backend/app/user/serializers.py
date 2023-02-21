from rest_framework_simplejwt.serializers import (
    TokenObtainPairSerializer,
    TokenRefreshSerializer,
)


class PairTokenSerializer(TokenObtainPairSerializer):
    """Custom TokenObtainPairSerializer to return JSON:API response format"""

    def validate(self, attrs):
        """JSON:API response format"""
        data = super().validate(attrs)
        access = data["access"]
        refresh = data["refresh"]
        response = {
            "data": {
                "type": "token",
                "attributes": {
                    "access": access,
                    "refresh": refresh,
                },
            }
        }
        return response


class RefreshTokenSerializer(TokenRefreshSerializer):
    """Custom TokenRefreshSerializer to return JSON:API response format"""

    def validate(self, attrs):
        """JSON:API response format"""
        data = super().validate(attrs)
        access = data["access"]
        response = {
            "data": {
                "type": "token",
                "attributes": {
                    "access": access,
                },
            }
        }
        return response
