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

    def create(self, validated_data):
        groups = validated_data.pop("groups", [])
        user_permissions = validated_data.pop("user_permissions", [])

        user = models.User(
            email=validated_data["email"],
            phone_no=validated_data.get("phone_no"),
            first_name=validated_data.get("first_name", ""),
            last_name=validated_data.get("last_name", "")
        )
        user.set_password(validated_data["password"])
        user.save()

        # Assign groups and permissions
        user.groups.set(groups)
        user.user_permissions.set(user_permissions)

        return user

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        groups = validated_data.pop("groups", None)
        user_permissions = validated_data.pop("user_permissions", None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if password:
            instance.set_password(password)

        instance.save()

        # Update groups and permissions if provided
        if groups is not None:
            instance.groups.set(groups)
        if user_permissions is not None:
            instance.user_permissions.set(user_permissions)

        return instance