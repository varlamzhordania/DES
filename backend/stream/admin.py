from django.contrib import admin
from .models import UserRoom


# Register your models here.
class UserRoomAdmin(admin.ModelAdmin):
    list_display = ('id', "user", "is_active", "is_busy", "update_at")
    list_filter = ("is_active", "is_busy", "update_at")


admin.site.register(UserRoom, UserRoomAdmin)
