from django.contrib import admin
from .models import Cart, CartItem, Extra, Tip, Order, OrderItem


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


class OrderItemInline(admin.StackedInline):
    model = OrderItem
    extra = 0


class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "payment_method", "payment_status", "create_at", "update_at")
    list_filter = ("payment_method", "payment_status", "create_at", "update_at")
    search_fields = ("id",)
    inlines = [OrderItemInline]
    readonly_fields = ["create_at", "update_at", 'session_id', 'session_customer']


class OrderItemAdmin(admin.ModelAdmin):
    list_display = ("id", "order", 'food', 'quantity', 'price')


admin.site.register(Extra, ExtraAdmin)
admin.site.register(Tip, TipAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem, CartItemAdmin)
admin.site.register(Order, OrderAdmin)
# admin.site.register(OrderItem, OrderItemAdmin)
