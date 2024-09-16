from django.contrib.auth.password_validation import validate_password
from django.core import exceptions
from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    """Serializer for custom user model."""

    class Meta:
        model = User
        fields = (
            "email",
            "phone_no",
            "first_name",
            "last_name",
        )


class UserPasswordValidatorMixin:
    """Mixin serializer class for password validation."""

    def validate_password(self, data):
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

class UserRegistrationSerializer(serializers.ModelSerializer, UserPasswordValidatorMixin):
    """Serializer for user registration."""

    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = (
            "email",
            "first_name",
            "last_name",
            "phone_no",
            "password1",
            "password2",
        )

    def validate(self, data):
        self.validate_password(data)
        return super().validate(data)

    def create(self, validated_data):
        user = User(
            email=validated_data["email"],
            first_name=validated_data.get("first_name", ""),
            last_name=validated_data.get("last_name", ""),
            phone_no=validated_data.get("phone_no", ""),
        )
        user.set_password(validated_data["password1"])
        user.save()
        return user


class UserUpdateSerializer(serializers.ModelSerializer):
    """Serializer for user data updation."""

    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "email",
            "phone_no",
        )

    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance


class UserPasswordUpdateSerializer(serializers.ModelSerializer, UserPasswordValidatorMixin):
    """Serializer for user pasword updation."""

    old_password = serializers.CharField(write_only=True)
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = (
            "old_password",
            "password1",
            "password2",
        )

    def validate_old_password(self, old_password):
        user = self.instance
        if not user.check_password(old_password):
            raise serializers.ValidationError({"old_password": "Old password is incorrect"})
        return old_password

    def validate(self, data):
        self.validate_password(data)
        return super().validate(data)

    def update(self, instance, validated_data):
        instance.set_password(validated_data["password1"])
        instance.save()
        return instance