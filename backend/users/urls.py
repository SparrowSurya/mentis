from django.urls import path

from . import views


urlpatterns = [
    path("", views.root, name="root"),

    path("user/register", views.UserRegistrationAPIView.as_view(), name="user-register"),

    path('user/login', views.UserLoginAPIView.as_view(), name='user-login'),
    path('user/logout', views.UserLogoutAPIView.as_view(), name='user-logout'),
    path('token/refresh/', views.UserTokenRefreshView.as_view(), name='user-token-refresh'),

]