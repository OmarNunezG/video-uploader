from rest_framework.urls import path
from user import views

app_name = "user"

urlpatterns = (
    path("token/", views.PairTokenView.as_view(), name="pair-token"),
    path(
        "token/refresh/",
        views.RefreshTokenView.as_view(),
        name="refresh-token",
    ),
    path("", views.UserListView.as_view(), name="list"),
    path("<int:user_id>/", views.UserDetailView.as_view(), name="detail"),
    path(
        "<int:user_id>/videos/",
        views.UserVideosView.as_view(),
        name="videos",
    ),
    path("profile/", views.UserProfileView.as_view(), name="profile"),
)
