from rest_framework import status, generics
from rest_framework.decorators import api_view
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from . import serializers


@api_view(["GET"])
def root(request):
    return Response("Welcome to the mentis project API.")


class UserRegistrationAPIView(generics.GenericAPIView):
    """User Registration API view."""

    serializer_class = serializers.UserRegistrationSerializer
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        return Response("API endpoint for user registration.", status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            user = serializer.save()
            user_serializer = serializers.UserSerializer(user)
            return Response(user_serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginAPIView(TokenObtainPairView):
    """User login API view."""


class UserLogoutAPIView(generics.GenericAPIView):
    """User logout API view."""

    def post(self, request, *args, **kwargs):
        try:
            refresh_token = request.data["refresh"]
            RefreshToken(refresh_token).blacklist()
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_205_RESET_CONTENT)

class UserTokenRefreshView(TokenRefreshView):
    """User refresh access token API view."""