from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from comment import serializers
from core import models


class CommentDetailView(APIView):
    """
    Comment view for retrieving, updating and deleting a comment
    Allowed methods: GET, PATCH, DELETE
    """

    serializer_class = serializers.CommentSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = models.Comment.objects

    def get(self, request, id, format=None):
        """Retrieve a comment"""

        try:
            comment = self.queryset.get(id=id)
            serializer = self.serializer_class(comment, many=False)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except models.Comment.DoesNotExist:
            """Return 404 if comment not found"""

            response = {
                "status": "404",
                "title": "Not Found",
                "detail": "Comment not found",
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)
        except Exception:
            """Return 500 if server error"""

            response = {
                "status": "500",
                "title": "Internal Server Error",
                "detail": "Server error",
            }
            return Response(
                response, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def patch(self, request, id, format=None):
        """Update a comment"""

        try:
            comment = self.queryset.get(id=id)
            user = request.user

            if comment.created_by != user:
                """Return 403 if user is not comment creator"""

                response = {
                    "status": "403",
                    "title": "Forbidden",
                    "detail": "You are not the comment creator",
                }
                return Response(response, status=status.HTTP_403_FORBIDDEN)

            serializer = self.serializer_class(
                comment, data=request.data, partial=True
            )
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )
        except models.Comment.DoesNotExist:
            """Return 404 if comment not found"""

            response = {
                "status": "404",
                "title": "Not Found",
                "detail": "Comment not found",
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)
        except Exception:
            """Return 500 if server error"""

            response = {
                "status": "500",
                "title": "Internal Server Error",
                "detail": "Server error",
            }
            return Response(
                response, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def delete(self, request, id, format=None):
        """Delete a comment"""

        try:
            comment = self.queryset.get(id=id)
            user = request.user

            if comment.created_by != user:
                """Return 403 if user is not comment creator"""

                response = {
                    "status": "403",
                    "title": "Forbidden",
                    "detail": "You are not the comment creator",
                }
                return Response(response, status=status.HTTP_403_FORBIDDEN)

            comment.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except models.Comment.DoesNotExist:
            """Return 404 if comment not found"""

            response = {
                "status": "404",
                "title": "Not Found",
                "detail": "Comment not found",
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)
        except Exception:
            """Return 500 if server error"""

            response = {
                "status": "500",
                "title": "Internal Server Error",
                "detail": "Server error",
            }
            return Response(
                response, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
