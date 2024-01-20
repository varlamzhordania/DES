from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


class CustomUserAdmin(UserAdmin):
    model = User
    list_display = (
        "id", "username", "is_staff", "is_superuser", "is_active", "is_online")
    list_filter = ("is_staff", "is_active", "is_online")
    search_fields = ("id", "username",)
    ordering = ("-is_online", "-id")


admin.site.register(User, CustomUserAdmin)
