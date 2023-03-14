from django.urls import path
from reply import views

app_name = "reply"

urlpatterns = [
    path("<int:id>/", views.ReplyDetail.as_view(), name="detail"),
]
