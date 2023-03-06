from django.urls import path
from comment import views

app_name = "comment"

urlpatterns = [
    path("<int:id>/", views.CommentDetailView.as_view(), name="detail"),
]
