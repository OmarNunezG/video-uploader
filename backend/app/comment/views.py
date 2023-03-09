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


class LikeView(APIView):
    """
    Comment like view for counting, liking and disliking comments
    Allowed methods: GET, POST, DELETE
    """

    serializer_class = serializers.LikeSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = models.CommentLike.objects

    def get(self, request, id, format=None):
        """Count likes for a comment"""

        try:
            comment = models.Comment.objects.get(id=id)
            likes = comment.likes
            response = {"likes": likes}
            return Response(response, status=status.HTTP_200_OK)
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

    def post(self, request, id, format=None):
        """Like a comment"""

        try:
            data = request.data
            if data:
                """Return 400 if data is not empty"""

                response = {
                    "status": "400",
                    "title": "Bad Request",
                    "detail": "Data is not required",
                }
                return Response(response, status=status.HTTP_400_BAD_REQUEST)

            comment = models.Comment.objects.get(id=id)
            user = request.user

            if comment.created_by == user:
                """Return 403 if user is comment creator"""

                response = {
                    "status": "403",
                    "title": "Forbidden",
                    "detail": "You are the comment creator",
                }
                return Response(response, status=status.HTTP_403_FORBIDDEN)

            like = self.queryset.filter(comment=comment, liked_by=user)
            if like.exists():
                """Return 400 if user already liked the comment"""

                response = {
                    "status": "400",
                    "title": "Bad Request",
                    "detail": "You already liked this comment",
                }
                return Response(response, status=status.HTTP_400_BAD_REQUEST)

            data = {"comment": id, "liked_by": user.id}
            serializer = self.serializer_class(data=data, many=False)

            if not serializer.is_valid():
                """Return 400 if serializer is not valid"""

                return Response(
                    serializer.errors, status=status.HTTP_400_BAD_REQUEST
                )

            serializer.save()
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

    def delete(self, request, id, format=None):
        """Dislike a comment"""

        try:
            data = request.data
            if data:
                """Return 400 if data is not empty"""

                response = {
                    "status": "400",
                    "title": "Bad Request",
                    "detail": "Data is not required",
                }
                return Response(response, status=status.HTTP_400_BAD_REQUEST)

            comment = models.Comment.objects.get(id=id)
            user = request.user

            if comment.created_by == user:
                """Return 403 if user is comment creator"""

                response = {
                    "status": "403",
                    "title": "Forbidden",
                    "detail": "You are the comment creator",
                }
                return Response(response, status=status.HTTP_403_FORBIDDEN)

            like = self.queryset.filter(comment=comment, liked_by=user)
            if not like.exists():
                """Return 400 if user did not like the comment"""

                response = {
                    "status": "400",
                    "title": "Bad Request",
                    "detail": "You did not like this comment",
                }
                return Response(response, status=status.HTTP_400_BAD_REQUEST)

            serializer = self.serializer_class()
            serializer.delete(like.first())
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
