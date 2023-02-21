from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from user import serializers


class PairTokenView(TokenObtainPairView):
    """Custom TokenObtainPairView to return JSON:API response format"""

    serializer_class = serializers.PairTokenSerializer


class RefreshTokenView(TokenRefreshView):
    """Custom TokenRefreshView to return JSON:API response format"""

    serializer_class = serializers.RefreshTokenSerializer
