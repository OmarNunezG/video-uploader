from rest_framework.urls import path
from user import views

app_name = "user"

urlpatterns = (
    path("token/", views.PairTokenView.as_view(), name="token_obtain_pair"),
    path(
        "token/refresh/",
        views.RefreshTokenView.as_view(),
        name="token_refresh",
    ),
)
