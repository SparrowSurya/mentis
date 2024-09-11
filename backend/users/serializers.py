from django.contrib.auth.password_validation import validate_password
from django.core import exceptions
from rest_framework import serializers

from . import models


class UserSerializer(serializers.ModelSerializer):
    """Serializer for custom user model."""

    class Meta:
        model = models.User
        fields = (
            "id",
            "password",
            "last_login",
            "is_superuser",
            "email",
            "phone_no",
            "first_name",
            "last_name",
            "is_staff",
            "is_active",
            "date_joined",
            "groups",
            "user_permissions",
        )
        read_only_fields = (
            "id",
            "is_staff",
            "is_superuser",
            "is_active",
            "date_joined",
            "last_login",
            "groups",
            "user_permissions",
        )
        extra_kwargs = {
            "password": {"write_only": True},
        }


class UserRegistrationSerializer(serializers.ModelSerializer):
    """Serializer for user registration."""

    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = models.User
        fields = (
            "email",
            "first_name",
            "last_name",
            "phone_no",
            "password1",
            "password2",
        )

    def validate(self, data):
        """
        * Check password1 equals password2.
        * django password validation.
        """
        pswd1 = data["password1"]
        pswd2 = data["password2"]

        if pswd1 != pswd2:
            raise serializers.ValidationError("password1 do not matches password2.")

        error = None
        try:
            validate_password(password=pswd1, user=None)
        except exceptions.ValidationError as e:
            error = e

        if error:
            raise serializers.ValidationError(error)

        return super().validate(data)

    def create(self, validated_data):
        user = models.User(
            email=validated_data["email"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
            phone_no=validated_data["phone_no"],
        )
        user.set_password(validated_data["password1"])
        user.save()
        return user
