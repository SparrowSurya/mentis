from rest_framework import status, generics
from rest_framework.decorators import api_view
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from . import serializers


@api_view(["GET"])
def root(request):
    return Response("Welcome to the mentis project API.")


class UserRegistrationAPIView(generics.GenericAPIView):
    """User Registration API view."""

    serializer_class = serializers.UserSerializer
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        return Response("API url endpoint for user registration.", status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            serializer.save()
            return Response({"user": serializer.data}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
