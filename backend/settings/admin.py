from django.contrib import admin
from .models import Theme, Setting, PaymentGateway


# Register your models here.


class ThemeAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "is_primary"]
    list_filter = ["is_primary"]
    search_fields = ["id", "name"]


class SettingAdmin(admin.ModelAdmin):
    list_display = ["id", "company_name", "payment_gateways","logo", "logo_mini", "payment_gateways"]


class PaymentGatewayAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "create_at", "update_at"]


admin.site.register(Theme, ThemeAdmin)
admin.site.register(Setting, SettingAdmin)
admin.site.register(PaymentGateway, PaymentGatewayAdmin)
