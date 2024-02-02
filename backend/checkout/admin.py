from django.contrib import admin
from .models import Cart, CartItem, Extra, Tip


# Register your models here.

class ExtraAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "price", "is_active", "create_at", "update_at")
    list_filter = ("is_active", "create_at", "update_at")
    search_fields = ("id", "name")


class TipAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "amount", "is_active", "create_at", "update_at")
    list_filter = ("is_active", "create_at", "update_at")
    search_fields = ("id", "name")


class CartAdmin(admin.ModelAdmin):
    list_display = ("id", 'user')


class CartItemAdmin(admin.ModelAdmin):
    list_display = ("id", "cart", 'food', 'quantity')


admin.site.register(Extra, ExtraAdmin)
admin.site.register(Tip, TipAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem, CartItemAdmin)
