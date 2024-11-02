from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from . import models


@admin.register(models.User)
class UserAdmin(BaseUserAdmin):
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "phone",
                    "department",
                    "first_name",
                    "last_name",
                    "staff_member",
                    "active_member",
                    "password1",
                    "password2",
                ),
            },
        ),
    )
    fieldsets = (
        (None, {"fields": ("phone", "password")}),
        (
            "Personal info",
            {
                "fields": (
                    "department",
                    "first_name",
                    "last_name",
                    "staff_member",
                    "active_member",
                )
            },
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )
    list_display = ["id", "phone", "staff_member", "active_member", "section"]
    list_editable = ["phone", "staff_member", "section"]
    list_per_page = 10
    search_fields = ["phone", "staff_member", "section"]
    list_filter = ["phone", "staff_member", "section"]
    list_select_related = ["section"]
    ordering = ["id"]


@admin.register(models.Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]


@admin.register(models.OtpCode)
class OtpCodeAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "code"]


@admin.register(models.OneTimeLink)
class OneTimeLinkAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "uuid"]
