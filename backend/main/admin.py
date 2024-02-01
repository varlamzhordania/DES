from django.contrib import admin
from .models import Category, Food


# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "description", "is_active", "create_at", "update_at")
    list_filter = ("is_active", "create_at", "update_at")
    search_fields = ("id", "name")


class FoodAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "category", "price", "is_active", "create_at", "update_at")
    list_filter = ("is_active", "create_at", "update_at", "category")
    search_fields = ("id", "name")


admin.site.register(Category, CategoryAdmin)
admin.site.register(Food, FoodAdmin)
