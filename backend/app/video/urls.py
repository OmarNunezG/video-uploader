from rest_framework.urls import path
from video import views

app_name = "video"

urlpatterns = [
    path("", views.VideoList.as_view(), name="list"),
    path("<int:id>/", views.VideoDetailView.as_view(), name="detail"),
    path(
        "<int:id>/comments/", views.CommentListView.as_view(), name="comment"
    ),
    path("<int:id>/likes/", views.LikeListView.as_view(), name="like"),
]
