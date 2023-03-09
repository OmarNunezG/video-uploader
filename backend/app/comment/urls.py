from django.urls import path
from comment import views

app_name = "comment"

urlpatterns = [
    path("<int:id>/", views.CommentDetailView.as_view(), name="detail"),
    path("<int:id>/likes/", views.LikeView.as_view(), name="like"),
]
