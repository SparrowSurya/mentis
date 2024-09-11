from django.urls import path

from . import views


urlpatterns = [
    path("", views.root, name="root"),

    path("user/register", views.UserRegistrationAPIView.as_view(), name="user-register"),
]