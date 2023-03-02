from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import permissions, status
from rest_framework.exceptions import NotFound
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from core import models
from user import serializers


def user_detail_url(user_id):
    """Get user URL"""

    return reverse("user:detail", args=[user_id])


class PairTokenView(TokenObtainPairView):
    """
    Pair token view
    Allowed methods: POST
    """

    serializer_class = serializers.PairTokenSerializer


class RefreshTokenView(TokenRefreshView):
    """
    Refresh token view
    Allowed methods: POST
    """

    serializer_class = serializers.RefreshTokenSerializer


class UserListView(APIView):
    """
    User view for listing and creating users
    Allowed methods: GET, POST
    """

    serializer_class = serializers.UserSerializer
    permission_classes = (permissions.AllowAny,)
    pagination_class = PageNumberPagination
    queryset = get_user_model().objects

    def get(self, request, format=None):
        """
        List all users with pagination
        """

        try:
            users = self.queryset.all().order_by("-id")

            params = request.query_params
            if "username" in params:
                users = users.filter(username__icontains=params["username"])

            paginator = self.pagination_class()

            page = paginator.paginate_queryset(users, request)
            serializer = self.serializer_class(page, many=True)
            response = serializer.data

            return Response(response, status=status.HTTP_200_OK)
        except NotFound:
            """Return 404 Not Found if there are no users"""

            response = {
                "status": "404",
                "title": "Not Found",
                "detail": "The requested page is not available",
            }
            return Response(
                response,
                status=status.HTTP_404_NOT_FOUND,
            )
        except Exception:
            """Return 500 Internal Server Error if there was an error"""

            response = {
                "status": "500",
                "title": "Internal Server Error",
                "detail": "There was an error listing the users",
            }
            return Response(
                response,
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def post(self, request, format=None):
        """
        Create a new user and return its location in the Location header
        and a JSON:API response format
        """

        try:
            data = request.data
            attributes = data.get("attributes")
            if not attributes:
                response = {
                    "status": "400",
                    "title": "Bad Request",
                    "detail": "The attributes field must be present",
                }
                return Response(response, status=status.HTTP_400_BAD_REQUEST)

            serializer = self.serializer_class(data=attributes, many=False)
            if not serializer.is_valid():
                response = {
                    "status": "400",
                    "title": "Bad Request",
                    "detail": serializer.errors,
                }
                return Response(response, status=status.HTTP_400_BAD_REQUEST)

            serializer.save()

            response = serializer.data
            headers = {
                "Location": user_detail_url(response["id"]),
            }
            return Response(
                response,
                status=status.HTTP_201_CREATED,
                headers=headers,
            )
        except Exception:
            """Return 500 Internal Server Error if there was an error"""

            response = {
                "status": "500",
                "title": "Internal Server Error",
                "detail": "There was an error creating the user",
            }
            return Response(
                response,
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class UserDetailView(APIView):
    """
    User view for retrieve, update and delete specific user
    Allowed methods: GET, PATCH, DELETE
    """

    serializer_class = serializers.UserSerializer
    permission_classes = (permissions.IsAdminUser,)
    queryset = get_user_model().objects

    def get(self, request, user_id, format=None):
        """Get a user and link"""

        try:
            user = self.queryset.get(id=user_id)
            serializer = self.serializer_class(user, many=False)

            response = serializer.data
            return Response(
                response,
                status=status.HTTP_200_OK,
            )
        except get_user_model().DoesNotExist:
            """Return 404 Not Found if user not found"""

            response = {
                "status": "404",
                "title": "Not Found",
                "detail": "User not found",
            }
            return Response(
                response,
                status=status.HTTP_404_NOT_FOUND,
            )
        except Exception:
            """Return 500 Internal Server Error if there was an error"""

            response = {
                "status": "500",
                "title": "Internal Server Error",
                "detail": "There was an error retrieving the user",
            }
            return Response(
                response,
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def patch(self, request, user_id, format=None):
        """Update a user and return its location in the Location header"""

        try:
            data = request.data
            attributes = data.get("attributes")
            if not attributes:
                response = {
                    "status": "400",
                    "title": "Bad Request",
                    "detail": "The attributes field must be present",
                }
                return Response(response, status=status.HTTP_400_BAD_REQUEST)

            user = self.queryset.get(id=user_id)
            serializer = self.serializer_class(
                user, data=attributes, many=False, partial=True
            )
            if not serializer.is_valid():
                response = {
                    "status": "400",
                    "title": "Bad Request",
                    "detail": serializer.errors,
                }
                return Response(response, status=status.HTTP_400_BAD_REQUEST)

            serializer.save()
            headers = {
                "Location": user_detail_url(user_id),
            }

            response = serializer.data
            return Response(
                response, status=status.HTTP_200_OK, headers=headers
            )
        except get_user_model().DoesNotExist:
            """Return 404 status code if user not found"""

            response = {
                "status": "404",
                "title": "Not Found",
                "detail": "User not found",
            }
            return Response(
                response,
                status=status.HTTP_404_NOT_FOUND,
            )
        except Exception:
            """Return 500 status code if there was an error"""

            response = {
                "status": "500",
                "title": "Internal Server Error",
                "detail": "There was an error updating the user",
            }
            return Response(
                response,
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def delete(self, request, user_id, format=None):
        """Delete a user and return 204 status code"""

        try:
            user = self.queryset.get(id=user_id)
            user.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except get_user_model().DoesNotExist:
            """Return 404 status code if user not found"""

            response = {
                "status": "404",
                "title": "Not Found",
                "detail": "User not found",
            }
            return Response(
                response,
                status=status.HTTP_404_NOT_FOUND,
            )
        except Exception:
            """Return 500 status code if there was an error"""

            response = {
                "status": "500",
                "title": "Internal Server Error",
                "detail": "There was an error deleting the user",
            }
            return Response(
                response,
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class UserProfileView(APIView):
    """
    View for retrieving and updating the current user profile
    Allowed methods: GET, PATCH
    """

    serializer_class = serializers.UserSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, format=None):
        """
        Get the current user profile
        and return it with 200 status code
        """

        try:
            params = request.query_params
            if params:
                response = {
                    "status": "400",
                    "title": "Bad Request",
                    "detail": "This endpoint does not accept query parameters",
                }
                return Response(response, status=status.HTTP_400_BAD_REQUEST)

            user = request.user
            serializer = self.serializer_class(user, many=False)

            response = serializer.data
            return Response(response, status=status.HTTP_200_OK)
        except Exception:
            """Return 500 status code if there was an error"""

            response = {
                "status": "500",
                "title": "Internal Server Error",
                "detail": "There was an error retrieving your profile",
            }
            return Response(
                response,
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def patch(self, request, format=None):
        """Update the current user profile"""

        try:
            data = request.data
            attributes = data.get("attributes")
            if not attributes:
                response = {
                    "status": "400",
                    "title": "Bad Request",
                    "detail": "Missing attributes in request body",
                }
                return Response(response, status=status.HTTP_400_BAD_REQUEST)

            user = request.user
            serializer = self.serializer_class(
                user, data=attributes, partial=True
            )
            if not serializer.is_valid():
                response = {
                    "status": "400",
                    "title": "Bad Request",
                    "detail": serializer.errors,
                }
                return Response(response, status=status.HTTP_400_BAD_REQUEST)

            serializer.save()

            response = serializer.data
            headers = {
                "Location": user_detail_url(response["id"]),
            }

            return Response(
                response,
                status=status.HTTP_200_OK,
                headers=headers,
            )
        except Exception:
            """Return 500 status code if there was an error"""

            response = {
                "status": "500",
                "title": "Internal Server Error",
                "detail": "There was an error updating your profile",
            }
            return Response(
                response,
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class UserVideosView(APIView):
    """
    User videos view for retrieve the current user videos
    Allowed methods: GET
    """

    serializer_class = serializers.UserVideoSerializer
    permission_classes = (permissions.AllowAny,)
    pagination_class = PageNumberPagination
    # queryset = models.Video.objects

    def get(self, request, user_id, format=None):
        """
        Get the current user videos
        """

        try:
            params = request.query_params
            if params:
                response = {
                    "status": "400",
                    "title": "Bad Request",
                    "detail": "Query parameters not allowed",
                }
                return Response(response, status=status.HTTP_400_BAD_REQUEST)

            videos = models.Video.objects.filter(
                created_by__id=user_id
            ).order_by("-id")

            paginator = self.pagination_class()
            page = paginator.paginate_queryset(videos, request)

            serializer = self.serializer_class(page, many=True)
            response = serializer.data

            return Response(response, status=status.HTTP_200_OK)
        except get_user_model().DoesNotExist:
            """Return 404 status code if user not found"""

            response = {
                "status": "404",
                "title": "Not Found",
                "detail": "User not found",
            }
            return Response(
                response,
                status=status.HTTP_404_NOT_FOUND,
            )
        except Exception:
            """Return 500 status code if there was an error"""

            response = {
                "status": "500",
                "title": "Internal Server Error",
                "detail": "There was an error retrieving your videos",
            }
            return Response(
                response,
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
