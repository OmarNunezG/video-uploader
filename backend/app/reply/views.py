from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from core import models
from reply import serializers


class ReplyDetail(APIView):
    serializer_class = serializers.ReplySerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = models.CommentReply.objects

    def get(self, request, id, format=None):
        try:
            reply = self.queryset.get(id=id)
            serializer = self.serializer_class(reply)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except models.CommentReply.DoesNotExist:
            """Return a 404 response if the reply does not exist."""
            response = {
                "status": "404",
                "title": "Not found",
                "detail": "Could not find the reply",
            }
            return Response(
                response,
                status=status.HTTP_404_NOT_FOUND,
            )
        except Exception:
            """Return a 500 response if an unexpected error occurs."""
            response = {
                "status": "500",
                "title": "Internal server error",
                "detail": "An unexpected error occurred",
            }
            return Response(
                response,
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def patch(self, request, id, format=None):
        try:
            reply = self.queryset.get(id=id)
            if reply.created_by != request.user:
                """
                Return a 403 response if the user is not the
                creator of the reply.
                """
                response = {
                    "status": "403",
                    "title": "Forbidden",
                    "detail": "You are not the creator of this reply",
                }
                return Response(
                    response,
                    status=status.HTTP_403_FORBIDDEN,
                )

            serializer = self.serializer_class(
                reply, data=request.data, partial=True
            )
            if not serializer.is_valid():
                response = {
                    "status": "400",
                    "title": "Bad request",
                    "detail": serializer.errors,
                }
                return Response(response, status=status.HTTP_400_BAD_REQUEST)

            serializer.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except models.CommentReply.DoesNotExist:
            """Return a 404 response if the reply does not exist."""
            response = {
                "status": "404",
                "title": "Not found",
                "detail": "Could not find the reply",
            }
            return Response(
                response,
                status=status.HTTP_404_NOT_FOUND,
            )
        except Exception:
            """Return a 500 response if an unexpected error occurs."""
            response = {
                "status": "500",
                "title": "Internal server error",
                "detail": "An unexpected error occurred",
            }
            return Response(
                response,
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def delete(self, request, id, format=None):
        try:
            reply = self.queryset.get(id=id)
            if reply.created_by != request.user:
                """
                Return a 403 response if the user is not the
                creator of the reply.
                """
                response = {
                    "status": "403",
                    "title": "Forbidden",
                    "detail": "You are not the creator of this reply",
                }
                return Response(
                    response,
                    status=status.HTTP_403_FORBIDDEN,
                )

            reply.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except models.CommentReply.DoesNotExist:
            """Return a 404 response if the reply does not exist."""
            response = {
                "status": "404",
                "title": "Not found",
                "detail": "Could not find the reply",
            }
            return Response(
                response,
                status=status.HTTP_404_NOT_FOUND,
            )
        except Exception:
            """Return a 500 response if an unexpected error occurs."""
            response = {
                "status": "500",
                "title": "Internal server error",
                "detail": "An unexpected error occurred",
            }
            return Response(
                response,
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
