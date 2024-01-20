from django.contrib import admin
from .models import Theme


# Register your models here.


class ThemeAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "is_primary"]
    list_filter = ["is_primary"]
    search_fields = ["id", "name"]


admin.site.register(Theme, ThemeAdmin)
