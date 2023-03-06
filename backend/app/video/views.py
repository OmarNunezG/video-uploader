from django.urls import reverse
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly,
)
from core import models
from video import serializers


class VideoList(APIView):
    """
    Video view for listing and creating videos
    Allowed methods: GET, POST
    """

    serializer_class = serializers.VideoSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    pagination_class = PageNumberPagination
    queryset = models.Video.objects

    def get(self, request, format=None):
        """
        List all videos with pagination
        """

        try:
            videos = self.queryset.all().order_by("-id")

            params = request.query_params
            if "search" in params:
                videos = videos.filter(title__icontains=params["search"])

            paginator = self.pagination_class()
            page = paginator.paginate_queryset(videos, request)
            serializer = self.serializer_class(page, many=True)

            response = paginator.get_paginated_response(serializer.data)
            return Response(response.data, status=status.HTTP_200_OK)
        except Exception:
            response = {
                "status": "500",
                "title": "Internal Server Error",
                "detail": "There was an error listing the videos",
            }
            return Response(
                response,
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def post(self, request, format=None):
        """
        Create a video and return its location in the Location header
        and the video data in the body
        """

        try:
            data = request.data
            serializer = self.serializer_class(data=data, many=False)
            if not serializer.is_valid():
                response = {
                    "status": "400",
                    "title": "Bad Request",
                    "detail": serializer.errors,
                }
                return Response(
                    response,
                    status=status.HTTP_400_BAD_REQUEST,
                )

            user = request.user
            serializer.save(created_by=user)
            response = serializer.data
            headers = {
                "Location": reverse("video:detail", args=[response["id"]])
            }
            return Response(
                response,
                status=status.HTTP_201_CREATED,
                headers=headers,
            )
        except Exception:
            """Return a 500 error if there was an error creating the video"""

            response = {
                "status": "500",
                "title": "Internal Server Error",
                "detail": "There was an error creating the video",
            }
            return Response(
                response,
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class VideoDetailView(APIView):
    """
    Video view for retrieving, updating, and deleting videos
    Allowed methods: GET, PATCH, DELETE
    """

    serializer_class = serializers.VideoSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = models.Video.objects

    def get(self, request, id, format=None):
        """
        Retrieve a video
        """

        try:
            video = self.queryset.get(id=id)
            serializer = self.serializer_class(video, many=False)
            response = serializer.data
            return Response(response, status=status.HTTP_200_OK)
        except models.Video.DoesNotExist:
            response = {
                "status": "404",
                "title": "Not Found",
                "detail": "The video was not found",
            }
            return Response(
                response,
                status=status.HTTP_404_NOT_FOUND,
            )
        except Exception:
            response = {
                "status": "500",
                "title": "Internal Server Error",
                "detail": "There was an error retrieving the video",
            }
            return Response(
                response,
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def patch(self, request, id, format=None):
        """
        Partially update a video
        """

        try:
            user = request.user
            video = self.queryset.get(id=id)

            if video.created_by != user:
                response = {
                    "status": "403",
                    "title": "Forbidden",
                    "detail": "You do not have permission to update"
                    + " this video",
                }
                return Response(
                    response,
                    status=status.HTTP_403_FORBIDDEN,
                )

            data = request.data
            serializer = self.serializer_class(
                video, data=data, many=False, partial=True
            )
            if not serializer.is_valid():
                response = {
                    "status": "400",
                    "title": "Bad Request",
                    "detail": serializer.errors,
                }
                return Response(
                    response,
                    status=status.HTTP_400_BAD_REQUEST,
                )

            serializer.save()

            response = serializer.data
            headers = {"Location": reverse("video:detail", args=[video.id])}
            return Response(
                response, status=status.HTTP_200_OK, headers=headers
            )

        except models.Video.DoesNotExist:
            """Return a 404 error if the video was not found"""

            response = {
                "status": "404",
                "title": "Not Found",
                "detail": "The video was not found",
            }
            return Response(
                response,
                status=status.HTTP_404_NOT_FOUND,
            )
        except Exception:
            """Return a 500 error if there was an error updating the video"""

            response = {
                "status": "500",
                "title": "Internal Server Error",
                "detail": "There was an error updating the video",
            }
            return Response(
                response,
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def delete(self, request, id, format=None):
        """
        Delete a video
        """

        try:
            user = request.user
            video = self.queryset.get(id=id)

            if video.created_by != user:
                response = {
                    "status": "403",
                    "title": "Forbidden",
                    "detail": "You do not have permission to delete"
                    + " this video",
                }
                return Response(
                    response,
                    status=status.HTTP_403_FORBIDDEN,
                )

            video.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except models.Video.DoesNotExist:
            """Return a 404 error if the video was not found"""

            response = {
                "status": "404",
                "title": "Not Found",
                "detail": "The video was not found",
            }
            return Response(
                response,
                status=status.HTTP_404_NOT_FOUND,
            )
        except Exception:
            """Return a 500 error if there was an error deleting the video"""

            response = {
                "status": "500",
                "title": "Internal Server Error",
                "detail": "There was an error deleting the video",
            }
            return Response(
                response,
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
