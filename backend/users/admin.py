from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from . import models


@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):

    list_display = ("email", "first_name", "last_name", "is_staff", "is_superuser")
    list_filter = ("is_staff", "is_superuser", "is_active", "groups")
    search_fields = ("phone_no", "first_name", "last_name", "email")
    ordering = ("date_joined",)
    readonly_fields = ("password", "last_login", "date_joined")
    fieldsets = (
        (None, {
            "fields": ("email", "password")

        }),
        (_("Personal info"), {
            "fields": ("first_name", "last_name", "phone_no")
        }),
        (_("Permissions"), {
            "fields": (
                "is_active",
                "is_staff",
                "is_superuser",
                "groups",
                "user_permissions",
            ),
        }),
        (_("Important dates"), {
            "fields": ("last_login", "date_joined")
        }),
    )
